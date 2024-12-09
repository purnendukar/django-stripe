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


class AbstractStripeProduct(AbstractStripeModel):
    """
    Products describe the specific goods or services you offer to your customers.
    For example, you might offer a Standard and
    Premium version of your goods or service;
    each version would be a separate Product.
    They can be used in conjunction with Prices
    to configure pricing in Payment Links, Checkout, and Subscriptions.
    Stripe documentation: https://stripe.com/docs/api/products
    """

    active = models.BooleanField(
        help_text=("Whether the product is currently available for purchase."),
    )
    description = models.TextField(
        null=True,
        help_text=(
            "The product’s description, meant to be displayable to the customer. "
            "Use this field to optionally store a long form explanation "
            "of the product being sold for your own rendering purposes."
        ),
    )
    name = models.CharField(
        max_length=255,
        help_text=(
            "The product’s name, meant to be displayable to the customer. "
            "Whenever this product is sold via a subscription, "
            "name will show up on associated invoice line item descriptions."
        ),
    )

    statement_descriptor = models.TextField(
        null=True,
        help_text=(
            "Extra information about a product which will appear "
            "on your customer’s credit card statement."
            "In the case that multiple products are billed at once, "
            "the first statement descriptor will be used."
        ),
    )
    tax_code = models.CharField(max_length=255, null=True, help_text="A tax code ID.")
    unit_label = models.CharField(
        max_length=255,
        null=True,
        help_text=(
            "A label that represents units of this product in Stripe"
            " and on customers’ receipts and invoices."
            "When set, this will be included in associated "
            "invoice line item descriptions."
        ),
    )
    images = LocalesField(
        models.CharField(max_length=255),
        size=8,
        default=list,
        help_text=(
            "A list of up to 8 URLs of images for this product, "
            "meant to be displayable to the customer."
        ),
    )
    shippable = models.BooleanField(
        null=True, help_text="Whether this product is shipped (i.e., physical goods)."
    )
    package_dimensions = models.JSONField(
        null=True,
        help_text="The dimensions of this product for shipping purposes.",
    )
    url = models.URLField(
        max_length=500,
        null=True,
        help_text="A URL of a publicly-accessible webpage for this product.",
    )
    created = models.BigIntegerField(
        help_text=(
            "Time at which the object was created. "
            "Measured in seconds since the Unix epoch"
        )
    )
    updated = models.BigIntegerField(
        help_text=(
            "Time at which the object was last updated. "
            "Measured in seconds since the Unix epoch"
        )
    )

    class Meta:
        abstract = True
