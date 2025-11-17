from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class Client(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="client_profile"
    )
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_de_naissance = models.DateField()
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)  # Ajouté pour cohérence login
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
    client = models.ForeignKey(
        Client, 
        on_delete=models.CASCADE,
        related_name="comptes"
    )
    solde = models.DecimalField(
    max_digits=20,
    decimal_places=2,
    default=Decimal("0.00")
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    
    def save(self, *args, **kwargs):
        if not self.num_compte:
            self.num_compte = f"CPT-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compte {self.num_compte} ({self.client})"

    class Meta:
        verbose_name = "Compte Bancaire"
        verbose_name_plural = "Comptes Bancaires"

class Operation(models.Model):
    compte = models.ForeignKey(
        CompteBancaire,
        on_delete=models.CASCADE,
        related_name="operations"
    )
    
    class TypeOperation(models.TextChoices):
        DEPOT = 'DEP', 'Dépôt'
        RETRAIT = 'RET', 'Retrait'
        
    type_operation = models.CharField(
        max_length=3,
        choices=TypeOperation.choices,
    )

    class StatutOperation(models.TextChoices):
        EN_ATTENTE = 'ATT', 'En attente'
        VALIDEE = 'VAL', 'Validée'
        ANNULEE = 'ANN', 'Annulée'

    statut = models.CharField(
        max_length=3,
        choices=StatutOperation.choices,
        default=StatutOperation.EN_ATTENTE
    )
    
    class SourceDepot(models.TextChoices):
        ESPECES = 'ESP', 'Espèces'
        CHEQUE = 'CHQ', 'Chèque'
        AUCUNE = 'NON', 'N/A'

    source = models.CharField(
        max_length=3,
        choices=SourceDepot.choices,
        default=SourceDepot.AUCUNE,
        blank=True
    )
        
    montant = models.DecimalField(
    max_digits=20,
    decimal_places=2,
    validators=[MinValueValidator(Decimal("0.01"))]
    )

    
    date_heure = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    
    date_validation = models.DateTimeField(
        null=True, 
        blank=True, 
        editable=False
    )

    def __str__(self):
        return f"{self.get_type_operation_display()} de {self.montant} MGA - {self.get_statut_display()}"

    class Meta:
        verbose_name = "Opération"
        verbose_name_plural = "Opérations"
        ordering = ['-date_heure']