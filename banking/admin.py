# banking/admin.py

from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from .models import Client, CompteBancaire, Operation

# Action custom pour valider les dépôts
@admin.action(description='Valider les dépôts sélectionnés')
def valider_depots(modeladmin, request, queryset):
    try:
        with transaction.atomic():
            depots_a_valider = queryset.filter(
                type_operation=Operation.TypeOperation.DEPOT,
                statut=Operation.StatutOperation.EN_ATTENTE
            )
            
            count = 0
            for op in depots_a_valider:
                compte = op.compte
                compte.solde += op.montant
                compte.save(update_fields=['solde'])  # Optimisé pour ne sauver que solde
                
                op.statut = Operation.StatutOperation.VALIDEE
                op.date_validation = timezone.now()
                op.save(update_fields=['statut', 'date_validation'])
                count += 1

            if count > 0:
                modeladmin.message_user(request, f"{count} dépôt(s) validés. Soldes mis à jour (ex: {depots_a_valider.first().compte.num_compte}).", messages.SUCCESS)
            else:
                modeladmin.message_user(request, "Aucun dépôt en attente sélectionné.", messages.WARNING)

    except Exception as e:
        modeladmin.message_user(request, f"Erreur validation : {str(e)}", messages.ERROR)

# Classe d'admin pour les Opérations
class OperationAdmin(admin.ModelAdmin):
    list_display = ('date_heure', 'compte', 'type_operation', 'montant', 'source', 'statut', 'date_validation')
    list_filter = ('statut', 'type_operation', 'source')
    search_fields = ('compte__num_compte', 'compte__client__user__username')
    actions = [valider_depots]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('compte', 'compte__client')

admin.site.register(Client)
admin.site.register(CompteBancaire)
admin.site.register(Operation, OperationAdmin)