# Third Party Stuff
from django.conf import settings

from django.db import models

if settings.DATABASES["default"]["ENGINE"].endswith("postgresql"):
    from django.contrib.postgres.fields import ArrayField
    LocalesField = ArrayField
else:
    class LocalesField(models.JSONField):
        def __init__(self, *args, **kwargs):
            kwargs.pop("size", None)
            return super().__init__(*args[1:], **kwargs)

# Django Stripe Stuff
from django_stripe.models.abstracts.mixins import AbstractStripeModel
from django_stripe.utils import Currency


class AbstractStripeCustomer(AbstractStripeModel):
    """
    Customer objects allow us to perform recurring charges and track multiple
    charges that are associated with the same customer
    Stripe documentation: https://stripe.com/docs/api/customers
    """

    EXEMPT = "exempt"
    REVERSE = "reverse"
    NONE = "none"

    TAX_EXEMPT_TYPES = ((EXEMPT, "Exempt"), (REVERSE, "Reverse"), (NONE, "None"))

    # contact details
    name = models.TextField(
        max_length=255,
        blank=True,
        help_text="The customer's full name or business name",
    )
    description = models.TextField(
        max_length=255,
        blank=True,
        help_text=(
            "An arbitrary string attached to the object. "
            "Often useful for displaying to users."
        ),
    )
    email = models.EmailField(blank=True, db_index=True)
    address = models.JSONField(
        null=True, blank=True, help_text="The customer's address"
    )

    balance = models.DecimalField(
        decimal_places=2,
        max_digits=9,
        null=True,
        blank=True,
        help_text=(
            "Current balance (in cents), if any, being stored on the customer's "
            "account. "
            "If negative, the customer has credit to apply to the next invoice. "
            "If positive, the customer has an amount owed that will be added to the "
            "next invoice. The balance does not refer to any unpaid invoices; it "
            "solely takes into account amounts that have yet to be successfully "
            "applied to any invoice. This balance is only taken into account for "
            "recurring billing purposes (i.e., subscriptions, invoices, invoice items)"
        ),
    )
    currency = models.CharField(
        choices=Currency.choices,
        default=Currency.USD.value,
        max_length=3,
        help_text=(
            "The currency the customer can be charged "
            "in for recurring billing purposes"
        ),
    )
    delinquent = models.BooleanField(
        default=False,
        help_text=(
            "Whether or not the latest charge for the "
            "customer's latest invoice has failed"
        ),
    )
    default_source = models.TextField(blank=True)
    shipping = models.JSONField(
        null=True,
        blank=True,
        help_text="Shipping information associated with the customer",
    )
    tax_exempt = models.CharField(
        choices=TAX_EXEMPT_TYPES,
        max_length=16,
        default=NONE,
        help_text="Describes the customer's tax exemption status. When set to reverse, "
        'invoice and receipt PDFs include the text "Reverse charge"',
    )
    preferred_locales = LocalesField(
        models.CharField(default="", blank=True, max_length=255),
        default=list,
        help_text=(
            "The customer's preferred locales (languages), ordered by preference"
        ),
    )

    invoice_prefix = models.CharField(
        default="",
        blank=True,
        max_length=255,
        help_text=(
            "The prefix for the customer used to generate unique invoice numbers"
        ),
    )
    invoice_settings = models.JSONField(
        null=True, blank=True, help_text="The customer's default invoice settings"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
