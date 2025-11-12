
from django.db import models
from django.core.validators import MinValueValidator
import uuid  # Pour un numéro de compte unique et non séquentiel

class Client(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    
    adresse = models.TextField(blank=True, null=True)

    #mila asina mdp
    
    email = models.EmailField(unique=True, help_text="Email du client")
    telephone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class CompteBancaire(models.Model):
    num_compte = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False, 
        help_text="Numéro de compte unique"
    )
    
    # Clé étrangère liant le compte au client
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,  # Si on supprime un client, ses comptes sont supprimés
        related_name="comptes"     # Permet d'accéder aux comptes via client.comptes.all()
    )
    
    solde = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,  # Date ajoutée automatiquement à la création
        editable=False
    )

    def save(self, *args, **kwargs):
        # Générer un numéro de compte unique si c'est un nouvel objet
        if not self.num_compte:
            # Génère un code simple, ex: "CPT-4A3B" (à adapter si besoin)
            self.num_compte = f"CPT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compte {self.num_compte} ({self.client})"

    class Meta:
        verbose_name = "Compte Bancaire"
        verbose_name_plural = "Comptes Bancaires"


class Operation(models.Model):
    # Operation_ID est géré par l'ID auto de Django
    
    # Clé étrangère liant l'opération au compte
    compte = models.ForeignKey(
        CompteBancaire,
        on_delete=models.CASCADE,  # Si le compte est supprimé, les opérations aussi
        related_name="operations"  # Accès via compte.operations.all()
    )

    class TypeOperation(models.TextChoices):
        DEPOT = 'DEP', 'Dépôt'
        RETRAIT = 'RET', 'Retrait'

    type_operation = models.CharField(
        max_length=3,
        choices=TypeOperation.choices,
    )
    
    montant = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]  # Le montant doit être positif
    )
    
    date_heure = models.DateTimeField(
        auto_now_add=True, # Horodatage automatique
        editable=False
    )

    def __str__(self):
        # 'get_type_operation_display' récupère le label lisible ('Dépôt' ou 'Retrait')
        return f"{self.get_type_operation_display()} de {self.montant}€ sur {self.compte.num_compte}"

    class Meta:
        verbose_name = "Opération"
        verbose_name_plural = "Opérations"
        ordering = ['-date_heure'] # Trier les opérations de la plus récente à la plus ancienne