from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from decimal import Decimal
from django.utils import timezone  # Corrigé pour now()
from .models import Client, CompteBancaire, Operation
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import Client, CompteBancaire, Operation
from django.http import JsonResponse, Http404

# === LOGIN ADMIN ===
def login_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Obligatoire pour admin
                login(request, user)
                messages.success(request, f"Bienvenue, {user.get_full_name() or user.username} !")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Accès refusé : vous n'êtes pas administrateur.")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'banking/login_admin.html')

# === DASHBOARD ADMIN ===
@staff_member_required(login_url='login_admin')
def admin_dashboard(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        # --- Créer un client ---
        if action == 'create_client':
            try:
                with transaction.atomic():
                    prenom = request.POST['prenom']
                    nom = request.POST['nom']
                    email = request.POST['email']
                    password = request.POST['password']
                    telephone = request.POST.get('telephone', '')
                    date_naissance = request.POST['date_naissance']

                    from django.contrib.auth.models import User
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        password=password,
                        first_name=prenom,
                        last_name=nom
                    )

                    client = Client.objects.create(
                        user=user,
                        prenom=prenom,
                        nom=nom,
                        email=email,
                        telephone=telephone,
                        date_de_naissance=date_naissance
                    )

                    compte = CompteBancaire(client=client)
                    compte.save()

                    messages.success(request, f"Client {prenom} {nom} créé ! Compte: {compte.num_compte}")
            except Exception as e:
                messages.error(request, f"Erreur : {e}")

        # --- Actions sur opérations ---
        elif action == 'bulk_action':
            op_ids = request.POST.getlist('op_ids')
            ops = Operation.objects.filter(id__in=op_ids, statut='ATT')

            if 'bulk_validate' in request.POST:
                _validate_operations(ops, request)
            elif 'bulk_refuse' in request.POST:
                _refuse_operations(ops, request)

            for key in request.POST:
                if key.startswith('validate_'):
                    op_id = key.split('_')[1]
                    op = get_object_or_404(Operation, id=op_id, statut='ATT')
                    _validate_operations([op], request)
                elif key.startswith('refuse_'):
                    op_id = key.split('_')[1]
                    op = get_object_or_404(Operation, id=op_id, statut='ATT')
                    _refuse_operations([op], request)

    # Données
    pending_ops = Operation.objects.filter(statut='ATT').select_related('compte', 'compte__client').order_by('-date_heure')
    recent_ops = Operation.objects.filter(statut='VAL').select_related('compte', 'compte__client').order_by('-date_validation')[:10]

    return render(request, 'banking/admin.html', {
        'pending_operations': pending_ops,
        'recent_operations': recent_ops,
    })

# Fonctions utilitaires
def _validate_operations(ops, request):
    count = 0
    for op in ops:
        with transaction.atomic():
            if op.type_operation == 'DEP':
                op.compte.solde += op.montant
            elif op.type_operation == 'RET':
                if op.compte.solde < op.montant:
                    messages.error(request, f"Retrait impossible : solde insuffisant ({op.compte.num_compte})")
                    continue
                op.compte.solde -= op.montant
            op.compte.save()
            op.statut = 'VAL'
            op.date_validation = timezone.now()
            op.save()
            count += 1
    if count:
        messages.success(request, f"{count} opération(s) validée(s).")

def _refuse_operations(ops, request):
    count = ops.update(statut='ANN', date_validation=timezone.now())
    if count:
        messages.success(request, f"{count} opération(s) refusée(s).")

def money_bag(request):
    return render(request, 'banking/money_bag.html')

def acceuil(request):
    return render(request, 'banking/acceuil.html')

def login_client(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        num_compte = request.POST.get('account', '').strip().upper()

        print(f"[DEBUG] Tentative login → Email: {email}, Compte: {num_compte}")

        try:
            # 1. Trouver le client par email
            client = Client.objects.get(email=email)
            
            # 2. Authentifier via User (email = username)
            user = authenticate(request, username=email, password=password)
            
            if user is not None and user.is_active:
                # 3. Vérifier que le numéro de compte correspond
                if client.comptes.filter(num_compte=num_compte).exists():
                    login(request, user)
                    messages.success(request, f"Connexion réussie ! Bienvenue {client.prenom}.")
                    return redirect('dash_client')
                else:
                    messages.error(request, "Numéro de compte incorrect.")
            else:
                messages.error(request, "Email ou mot de passe incorrect.")
                
        except Client.DoesNotExist:
            messages.error(request, "Aucun client trouvé avec cet email.")
    
    return render(request, 'banking/login_client.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('acceuil')

@login_required(login_url='login_client')
def dash_client(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    try:
        client = request.user.client_profile
        compte = client.comptes.first()
        
        if not compte:
            messages.error(request, "Aucun compte associé.")
            return redirect('acceuil')
        
        # Force refresh pour solde à jour (après admin)
        compte.refresh_from_db()
        
        # Charger ops à jour
        operations = compte.operations.all().order_by('-date_heure')[:20]

        if is_ajax and request.method == 'GET':
            ops_data = [
                {
                    'date_heure': op.date_heure.strftime('%d/%m/%Y %H:%M'),
                    'type_operation': op.get_type_operation_display(),
                    'montant': float(op.montant),
                    'type': op.type_operation,
                    'source': op.get_source_display(),
                    'statut': op.statut,
                    'statut_display': op.get_statut_display(),
                } for op in operations
            ]
            return JsonResponse({
                'success': True,
                'solde': float(compte.solde),
                'operations': ops_data
            })
        
        context = {
            'client': client,
            'compte': compte,
            'operations': operations
        }
        return render(request, 'banking/dash_client.html', context)
        
    except (Client.DoesNotExist, AttributeError):
        # Gérer cas où user n'a pas profil Client (ex: admin mal logué)
        if request.user.is_authenticated:
            logout(request)
        messages.error(request, "Erreur de session. Reconnectez-vous.")
        if is_ajax:
            return JsonResponse({'success': False, 'message': 'Erreur de session. Reconnectez-vous.'}, status=400)
        return redirect('login_client')

@login_required(login_url='login_client')
def depot_view(request):
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            montant_str = request.POST.get('montant')
            if not montant_str:
                raise ValueError('Le montant est manquant.')
                
            montant = Decimal(montant_str)
            num_compte = request.POST.get('num_compte')
            source = request.POST.get('source')
            
            if montant <= 0:
                raise ValueError('Montant invalide.')

            valid_sources = [Operation.SourceDepot.ESPECES, Operation.SourceDepot.CHEQUE]
            if source not in valid_sources:
                 raise ValueError('Source de dépôt invalide.')

            compte = get_object_or_404(
                CompteBancaire, 
                num_compte=num_compte, 
                client=request.user.client_profile
            )
            
            Operation.objects.create(
                compte=compte,
                type_operation=Operation.TypeOperation.DEPOT,
                montant=montant,
                source=source,
                statut=Operation.StatutOperation.EN_ATTENTE
            )
            
            success_message = f'Demande de dépôt {montant} MGA ({source}) en attente de validation.'
            messages.success(request, success_message)
            
            if is_ajax:
                operations = compte.operations.all().order_by('-date_heure')[:20]
                ops_data = [
                    {
                        'date_heure': op.date_heure.strftime('%d/%m/%Y %H:%M'),
                        'type_operation': op.get_type_operation_display(),
                        'montant': float(op.montant),
                        'type': op.type_operation,
                        'source': op.get_source_display(),
                        'statut': op.statut,
                        'statut_display': op.get_statut_display(),
                    } for op in operations
                ]
                return JsonResponse({
                    'success': True,
                    'message': success_message,
                    'solde': float(compte.solde),
                    'operations': ops_data
                })
            return redirect('dash_client')

        except (ValueError, Decimal.InvalidOperation, Http404) as e:
            error_message = str(e)
            messages.error(request, error_message)
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message}, status=400)
            return redirect('dash_client')
            
        except Exception as e:
            error_message = f'Erreur inattendue lors du dépôt: {e}'
            messages.error(request, error_message)
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message}, status=400)
            return redirect('dash_client')

    return redirect('dash_client')


@login_required(login_url='login_client')
@transaction.atomic
def retrait_view(request):  # Renommé pour cohérence URL
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            montant_str = request.POST.get('montant')
            if not montant_str:
                raise ValueError('Le montant est manquant.')
            montant = Decimal(montant_str)
            num_compte = request.POST.get('num_compte')

            if montant <= 0:
                raise ValueError('Montant invalide.')

            compte = get_object_or_404(CompteBancaire, num_compte=num_compte, client=request.user.client_profile)
            
            if compte.solde < montant:
                raise ValueError('Solde insuffisant.')
            
            compte.solde -= montant
            compte.save(update_fields=['solde'])
            
            Operation.objects.create(
                compte=compte,
                type_operation=Operation.TypeOperation.RETRAIT,
                montant=montant,
                statut=Operation.StatutOperation.VALIDEE,
                source=Operation.SourceDepot.AUCUNE,
                date_validation=timezone.now()
            )
            success_message = f'Retrait de {montant} MGA effectué.'
            messages.success(request, success_message)
                
            if is_ajax:
                operations = compte.operations.all().order_by('-date_heure')[:20]
                ops_data = [
                    {
                        'date_heure': op.date_heure.strftime('%d/%m/%Y %H:%M'),
                        'type_operation': op.get_type_operation_display(),
                        'montant': float(op.montant),
                        'type': op.type_operation,
                        'source': op.get_source_display(),
                        'statut': op.statut,
                        'statut_display': op.get_statut_display(),
                    } for op in operations
                ]
                return JsonResponse({
                    'success': True,
                    'message': success_message,
                    'solde': float(compte.solde),
                    'operations': ops_data
                })
            return redirect('dash_client')

        except (ValueError, Decimal.InvalidOperation, Http404) as e:
            error_message = str(e)
            messages.error(request, error_message)
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message}, status=400)
            return redirect('dash_client')
            
        except Exception as e:
            error_message = f'Erreur inattendue lors du retrait: {e}'
            messages.error(request, error_message)
            if is_ajax:
                return JsonResponse({'success': False, 'message': error_message}, status=400)
            return redirect('dash_client')
            
    return redirect('dash_client')