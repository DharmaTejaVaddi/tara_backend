from django.db import models
from Tara.settings.default import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo.models import ArrayField, EmbeddedField, JSONField
from .helpers import *
from usermanagement.models import Users, ServiceRequest
from docwallet.models import PrivateS3Storage
from servicetasks.models import ServiceTask
from usermanagement.models import *
from django.db.models import JSONField

class ProposedCompanyDetails(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                           related_name='proposed_company_details')
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_task = models.OneToOneField(ServiceTask, on_delete=models.CASCADE,
                                        related_name='service_task_proposed_company_details')

    proposed_company_names = JSONField(default=dict, blank=True, null=True)
    objectives_of_company = models.TextField(null=True, blank=True)
    business_activity_choices = [
        ('Agriculture', 'agriculture'),('Forestry', 'forestry'),('Fishing', 'fishing'),
        ('Mining And Quarrying', 'mining and quarrying'),('Construction', 'construction'),
        ('Manufacturing', 'Manufacturing'),('Education', 'education'),('Finance', 'finance'),
        ('Art And Entertainment', 'art and entertainment'),('Healthcare', 'healthcare'),
        ('Social Work', 'social work'),('Transport And Logistics', 'transport and logistics'),
        ('Electricity', 'electricity'),('Gas Supply', 'gas supply'),('Steam', 'steam'),
        ('Water Supply', 'water supply'), ('Waste Management', 'waste management'),
        ('Rental And Leasing Services', 'rental and leasing services'),
        ('Hotel And Restaurant', 'hotel and restaurant'),
        ('Information And Communication', 'information and communication'),
        ('Wholesale And Retail Trade','wholesale and retail trade'),
        ('Accommodation And Food Services', 'accommodation and food services'),
        ('Support Services', 'support services'),('Real Estate', 'real estate'),
        ('Financial Services', 'financial services'),('Fund Management', 'fund management'),
        ('Financial And Insurance Activities', 'financial and insurance activities'),
        ('Management Consultancy', 'management consultancy'),('Legal And Accounting', 'legal and accounting'),
        ('Business And Management Consultancy', 'business and management consultancy'),
        ('Other', 'Other')
    ]
    business_activity = models.CharField(max_length=255,choices=business_activity_choices, null=True, blank=True)
    nic_code = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.BigIntegerField()
    email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('sent for approval', 'Sent for Approval'),
            ('revoked', 'Revoked')
        ],
        default='in progress',
        null=False,
        blank=False
    )

    assignee = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_proposed_company_details'
    )
    reviewer = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_proposed_company_details'
    )

    def save(self, *args, **kwargs):
        # Default to service_task's values if not set
        if not self.assignee and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        company_names = self.proposed_company_names or {}
        return f"Proposed Company - {company_names.get('name_1', 'N/A')}"


class RegisteredOfficeAddressDetails(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                           related_name='registered_office_address')
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_task = models.OneToOneField(ServiceTask, on_delete=models.CASCADE,
                                        related_name='service_task_registered_office_address')

    OWNERSHIP_TYPE_CHOICES = [
        ('owned', 'Owned'),
        ('rented', 'Rented'),
        ('leased', 'Leased'),
    ]
    ownership_type = models.CharField(choices=OWNERSHIP_TYPE_CHOICES, max_length=255, null=True, blank=True)
    proposed_office_address = JSONField(default=dict, blank=True, null=True)

    utility_bill_file = models.FileField(upload_to=upload_utility_bill_file,
                                         null=True, blank=True, storage=PrivateS3Storage())
    NOC_file = models.FileField(upload_to=upload_noc_file,null=True, blank=True, storage=PrivateS3Storage())
    rent_agreement_file = models.FileField(upload_to=upload_rent_agreement_file,null=True, blank=True,
                                           storage=PrivateS3Storage())
    property_tax_receipt_file = models.FileField(upload_to=upload_property_tax_receipt_file,null=True, blank=True,
                                                 storage=PrivateS3Storage())
    status = models.CharField(
        max_length=20,
        choices=[
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('sent for approval', 'Sent for Approval'),
            ('revoked', 'Revoked')
        ],
        default='in progress',
        null=False,
        blank=False
    )

    assignee = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_registered_office_address_details'
    )
    reviewer = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_registered_office_address_details'
    )

    def save(self, *args, **kwargs):
        # Default to service_task's values if not set
        if not self.assignee and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        address = self.proposed_office_address or {}
        return f"Registered Office: {address.get('address_line_1', 'N/A')}, {address.get('city', 'N/A')}"


class AuthorizedPaidUpShareCapital(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                           related_name='authorized_capital_service_request')
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_task = models.OneToOneField(ServiceTask, on_delete=models.CASCADE,
                                        related_name='service_task_authorized_capital')
    authorized_share_capital = models.IntegerField(null=True)
    paid_up_share_capital = models.IntegerField(null=True)
    face_value_per_share = models.FloatField(null=True)
    no_of_shares = models.PositiveIntegerField()
    bank_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('sent for approval', 'Sent for Approval'),
            ('revoked', 'Revoked')
        ],
        default='in progress',
        null=False,
        blank=False
    )

    assignee = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='authorized_capital_assignee'
    )
    reviewer = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='authorized_capital_reviewer'
    )

    def save(self, *args, **kwargs):
        # Default to service_task's values if not set
        if not self.assignee and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Authorized: {self.authorized_share_capital}, Paid Up: {self.paid_up_share_capital}"


class Directors(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                           related_name='directors_details')
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_task = models.OneToOneField(
        ServiceTask,
        on_delete=models.CASCADE,
        related_name='service_task_directors_details'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('sent for approval', 'Sent for Approval'),
            ('revoked', 'Revoked')
        ],
        default='in progress'
    )
    assignee = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='assigned_directors_details')
    reviewer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='reviewed_directors_details')

    def save(self, *args, **kwargs):
        if not self.assignee and hasattr(self, 'service_task') and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and hasattr(self, 'service_task') and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Directors Details (ServiceRequest ID: {self.service_request.id})"


class DirectorsDetails(models.Model):
    directors_ref = models.ForeignKey(Directors,
                                      on_delete=models.CASCADE,
                                      related_name='directors'
                                      )
    director_first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    category_of_directorship_choices = [
        ('Executive Director', 'executive director'), ('Non-Executive Director', 'non-executive director'),
        ('Independent Director', 'independent director'), ('Nominee Director', 'nominee director'),
        ('Managing Director', 'managing director'), ('Whole Time Director', 'whole time director'),
        ('Alternate Director', 'alternate director'), ('Additional Director', 'additional director'),
        ('Small Shareholder Director', 'small shareholder director'),
        ('Chairman And Managing Director', 'chairman and managing director'),
        ('Professional Director', 'professional director'),
        ('Government Nominee Director', 'government nominee director'),
        ('Foreign National Director', 'foreign national director'), ('Resident Director', 'resident director'),
        ('Non-Resident Director', 'non-resident director'), ('Woman Director', 'woman director'),
        ('Other', 'other')
    ]

    category_of_directorship = models.CharField(max_length=100, choices=category_of_directorship_choices,
                                                blank=True, null=True)
    pan_card_file = models.FileField(upload_to=upload_pan_card_file,
                                     null=True, blank=True, storage=PrivateS3Storage())
    aadhaar_card_file = models.FileField(upload_to=upload_aadhaar_card_file,
                                         null=True, blank=True, storage=PrivateS3Storage())
    passport_photo_file = models.FileField(upload_to=upload_passport_photo_file,
                                           null=True, blank=True, storage=PrivateS3Storage())

    mobile_number = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True
    )

    nationality_choices = [('Indian', 'Indian'), ('Foreign National', 'Foreign National')]
    qualification_choices = [
        ('Below SSC', 'Below SSC'), ('SSC/Matriculation', 'SSC/Matriculation'),
        ('HSC/Intermediate/12th passed', 'HSC/Intermediate/12th passed'),
        ('Graduate', 'Graduate'), ('Post Graduate', 'Post Graduate'),
        ('Doctorate', 'Doctorate'), ('Professional Degree', 'Professional Degree'),
        ('Other', 'Other')
    ]
    residential_address_proof_choices = [
        ('Bank Statement', 'Bank Statement'), ('Utility Bill', 'Utility Bill'),
        ('Telephone/Mobile Bill', 'Telephone/Mobile Bill'),
        ('Electricity Bill', 'Electricity Bill'),
        ('Property Tax Receipt', 'Property Tax Receipt'),
        ('Lease/Rent Agreement', 'Lease/Rent Agreement')
    ]

    father_first_name = models.CharField(max_length=50)
    father_middle_name = models.CharField(max_length=50, blank=True)
    father_last_name = models.CharField(max_length=50)
    nationality = models.CharField(max_length=30, choices=nationality_choices, null=True, blank=True)
    area_of_occupation = models.CharField(max_length=30, null=True, blank=True)
    qualification = models.CharField(max_length=30, choices=qualification_choices, null=True, blank=True)

    residential_same_as_aadhaar_address = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    residential_address = models.TextField(blank=True, null=True)
    residential_address_proof = models.CharField(
        max_length=50, choices=residential_address_proof_choices, null=True, blank=True
    )
    residential_address_proof_file = models.FileField(
        upload_to=upload_residential_address_proof_file, null=True, blank=True
    )
    din_number = models.CharField(max_length=30, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True)
    din_number_value = models.CharField(max_length=30, blank=True, null=True)
    dsc = models.CharField(max_length=30, choices=[('Yes', 'Yes'), ('No', 'No')], null=True, blank=True)
    authorised_signatory_name = models.CharField(max_length=100, blank=True, null=True)
    details_of_existing_directorships = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True, null=True
    )
    existing_directorships_details = JSONField(default=list, blank=True, null=True)
    # Example structure for existing_directorships_details:
    # [
    #   {
    #     "company_name": "ABC Pvt Ltd",
    #     "cin": "U12345MH2023PTC000001",
    #     "type_of_company": "Private Limited",
    #     "position_held": "Director"
    #   },
    #   ...
    # ]
    form_dir2 = models.FileField(upload_to=upload_form_dir2, null=True, blank=True, storage=PrivateS3Storage())
    is_this_director_also_shareholder = models.CharField(max_length=3,
                                                         choices=[('Yes', 'Yes'), ('No', 'No')], default='No')
    no_of_shares = models.PositiveIntegerField(default=0, blank=True, null=True)
    shareholding_percentage = models.FloatField(null=True)
    paid_up_capital = models.IntegerField(null=True)
    specimen_signature_of_director = models.FileField(upload_to=upload_specimen_signature_of_director,
                                                      null=True, blank=True, storage=PrivateS3Storage())

    def __str__(self):
        return f"{self.director_first_name} {self.last_name}"



class Shareholders(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                           related_name='shareholders_details')
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_task = models.OneToOneField(
        ServiceTask,
        on_delete=models.CASCADE,
        related_name='service_task_shareholders_details'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('in progress', 'In Progress'),
            ('completed', 'Completed'),
            ('sent for approval', 'Sent for Approval'),
            ('revoked', 'Revoked')
        ],
        default='in progress'
    )
    assignee = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='assigned_shareholders_details')
    reviewer = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='reviewed_shareholders_details')

    def save(self, *args, **kwargs):
        if not self.assignee and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Shareholders Details (ServiceRequest ID: {self.service_request.id})"


class ShareholdersDetails(models.Model):
    shareholders_ref = models.ForeignKey(
        Shareholders, on_delete=models.CASCADE, related_name='shareholders'
    )
    shareholder_first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    shareholder_type_choices = [('Individual Indian Resident', 'individual indian resident'),
                                 ('Individual Non-Resident', 'individual non-resident'),
                                ('Individual Foreign National', 'individual foreign national'),
                                ('Body Corporate Indian Company', 'body corporate indian company'),
                                ('Body Corporate Foreign Company', 'body corporate foreign company'),
                                ('Limited Liability Partnership', 'limited liability partnership'),]

    shareholder_type = models.CharField(max_length=50, choices= shareholder_type_choices,
                                        default='Individual Indian Resident')
    mobile_number = models.BigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    pan_card_file = models.FileField(upload_to=upload_pan_card_file, null=True, blank=True,
                                     storage=PrivateS3Storage())
    aadhaar_card_file = models.FileField(upload_to=upload_aadhaar_card_file, null=True, blank=True,
                                    storage=PrivateS3Storage())
    bank_statement_file = models.FileField(upload_to=upload_bank_statement_file, null=True, blank=True,
                                             storage=PrivateS3Storage())
    shareholding_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    residential_same_as_aadhaar_address = models.CharField(
        max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], default='No'
    )
    residential_address = models.TextField(blank=True, null=True)
    residential_address_proof_choices = [
        ('Bank Statement', 'Bank Statement'), ('Utility Bill', 'Utility Bill'),
        ('Telephone/Mobile Bill', 'Telephone/Mobile Bill'),
        ('Electricity Bill', 'Electricity Bill'),
        ('Property Tax Receipt', 'Property Tax Receipt'),
        ('Lease/Rent Agreement', 'Lease/Rent Agreement')
    ]
    residential_address_proof = models.CharField(
        max_length=50, choices=residential_address_proof_choices, null=True, blank=True
    )
    residential_address_proof_file = models.FileField(
        upload_to=upload_residential_address_proof_file, null=True, blank=True
    )

    def __str__(self):
        return f"{self.shareholder_first_name} {self.last_name}"


class ReviewFilingCertificate(models.Model):
    service_type = models.CharField(max_length=20, default="Company Incorporation", editable=False)
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE,
                                            related_name='company_review_filing_certificate')
    service_task = models.OneToOneField(ServiceTask, on_delete=models.CASCADE,
                                        related_name='service_task_company_review_filing_certificate')

    FILING_STATUS_CHOICES = [
        ('in progress', 'In Progress'),
        ('filed', 'Filed'),
        ('resubmitted', 'Resubmitted'),
        ]
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resubmission', 'Resubmission'),
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
    ]
    review_certificate = models.FileField(upload_to=review_filing_certificate, null=True, blank=True,
                                          storage=PrivateS3Storage())
    status = models.CharField(max_length=20, choices=[('in progress', 'In Progress'), ('completed', 'Completed'),
                                        ('sent for approval', 'Sent for Approval'),('revoked', 'Revoked')],
                                         default='in progress', null=False,blank=False)

    filing_status = models.CharField(
        max_length=20,
        choices=FILING_STATUS_CHOICES,
        null=True,
        blank=True,
        default=None
    )
    approval_status = models.CharField(
        max_length=20,
        choices=APPROVAL_STATUS_CHOICES,
        null=True,
        blank=True,
        default=None
    )
    assignee = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_company_review_filing_certificate'
    )
    reviewer = models.ForeignKey(
        Users, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reviewed_company_review_filing_certificate'
    )

    def save(self, *args, **kwargs):
        # Default to service_request values if not set
        if not self.assignee and self.service_task.assignee:
            self.assignee = self.service_task.assignee
        if not self.reviewer and self.service_task.reviewer:
            self.reviewer = self.service_task.reviewer
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Review Filing Certificate for Service Request {self.service_request.id} - Status: {self.status}"


def calculate_completion_percentage(instance, exclude_fields=None):
    exclude_fields = exclude_fields or ['id', 'created_at', 'updated_at', 'service_request', 'service_task']
    total_fields = 0
    filled_fields = 0

    for field in instance._meta.fields:
        if field.name in exclude_fields:
            continue
        total_fields += 1
        value = getattr(instance, field.name)
        if value not in [None, '', []]:
            filled_fields += 1

    if total_fields == 0:
        return 0
    return round((filled_fields / total_fields) * 100)


@receiver(post_save, sender=ProposedCompanyDetails)
def sync_proposed_company_details_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()


@receiver(post_save, sender=RegisteredOfficeAddressDetails)
def sync_registered_office_address_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()


@receiver(post_save, sender=AuthorizedPaidUpShareCapital)
def sync_authorized_paid_up_capital_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()


@receiver(post_save, sender=Directors)
def sync_directors_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()

'''
@receiver(post_save, sender=Directors)
def auto_create_shareholders_from_directors(sender, instance, **kwargs):
    # Auto-create ShareholderDetails for directors marked as also being shareholders
    director = DirectorsDetails.objects.get(
        directors_ref=instance,
        is_this_director_also_shareholder='Yes'
    )

    if director:
        try:
            shareholder_details = Shareholders.objects.get(service_request=instance.directors_ref.service_request)
            already_exists = ShareholdersDetails.objects.get(
                shareholders_ref=shareholder_details,
                shareholder_first_name=director.director_first_name,
                last_name=director.last_name,
                email=director.email,
                mobile_number=director.mobile_number
            )
            if not already_exists:
                ShareholdersDetails.objects.create(
                    shareholders_ref=shareholder_details,
                    shareholder_first_name=director.director_first_name,
                    middle_name=director.middle_name,
                    last_name=director.last_name,
                    mobile_number=director.mobile_number,
                    email=director.email,
                    pan_card_file=director.pan_card_file,
                    aadhaar_card_file=director.aadhaar_card_file,
                    bank_statement_file=director.bank_statement_file,
                    shareholding_percentage=director.shareholding_percentage,
                    residential_same_as_aadhaar_address=director.residential_same_as_aadhaar_address,
                    residential_address=director.residential_address,
                    residential_address_proof=director.residential_address_proof,
                    residential_address_proof_file=director.residential_address_proof_file,
                    shareholder_type= "Individual Indian Resident"
                )
            else:
                # If already exists, you might want to update the existing record instead
                ShareholdersDetails.objects.update(
                    shareholders_ref=shareholder_details,
                    shareholder_first_name=director.director_first_name,
                    middle_name=director.middle_name,
                    last_name=director.last_name,
                    mobile_number=director.mobile_number,
                    email=director.email,
                    pan_card_file=director.pan_card_file,
                    aadhaar_card_file=director.aadhaar_card_file,
                    bank_statement_file=director.bank_statement_file,
                    shareholding_percentage=director.shareholding_percentage,
                    residential_same_as_aadhaar_address=director.residential_same_as_aadhaar_address,
                    residential_address=director.residential_address,
                    residential_address_proof=director.residential_address_proof,
                    residential_address_proof_file=director.residential_address_proof_file
                )

        except Shareholders.DoesNotExist:
            shareholder_details = Shareholders.objects.create(
                service_request=instance.directors_ref.service_request,
                service_task=instance.service_task,
                status='in progress')
            ShareholdersDetails.objects.create(
                shareholders_ref=shareholder_details,
                shareholder_first_name=director.director_first_name,
                middle_name=director.middle_name,
                last_name=director.director_last_name,
                mobile_number=director.mobile_number,
                email=director.email,
                pan_card_file=director.pan_card_file,
                aadhaar_card_file=director.aadhaar_card_file,
                bank_statement_file=director.bank_statement_file,
                shareholding_percentage=director.shareholding_percentage,
                residential_same_as_aadhaar_address=director.residential_same_as_aadhaar_address,
                residential_address=director.residential_address,
                residential_address_proof=director.residential_address_proof,
                residential_address_proof_file=director.residential_address_proof_file,
                shareholder_type="Individual Indian Resident"
            )
'''
@receiver(post_save, sender=Directors)
def auto_create_shareholders_from_directors(sender, instance, **kwargs):
    try:
        director = DirectorsDetails.objects.get(
            directors_ref=instance,
            is_this_director_also_shareholder='Yes'
        )

        if director:
            try:
                shareholder_details = Shareholders.objects.get(service_request=instance.service_request)
                already_exists = ShareholdersDetails.objects.filter(
                    shareholders_ref=shareholder_details,
                    shareholder_first_name=director.director_first_name,
                    last_name=director.last_name,
                    email=director.email,
                    mobile_number=director.mobile_number
                ).exists()

                if not already_exists:
                    ShareholdersDetails.objects.create(
                        shareholders_ref=shareholder_details,
                        shareholder_first_name=director.director_first_name,
                        middle_name=director.middle_name,
                        last_name=director.last_name,
                        mobile_number=director.mobile_number,
                        email=director.email,
                        pan_card_file=director.pan_card_file,
                        aadhaar_card_file=director.aadhaar_card_file,
                        bank_statement_file=director.bank_statement_file,
                        shareholding_percentage=director.shareholding_percentage,
                        residential_same_as_aadhaar_address=director.residential_same_as_aadhaar_address,
                        residential_address=director.residential_address,
                        residential_address_proof=director.residential_address_proof,
                        residential_address_proof_file=director.residential_address_proof_file,
                        shareholder_type="Individual Indian Resident"
                    )
                else:
                    existing = ShareholdersDetails.objects.get(
                        shareholders_ref=shareholder_details,
                        email=director.email
                    )
                    existing.shareholder_first_name = director.director_first_name
                    existing.middle_name = director.middle_name
                    existing.last_name = director.last_name
                    existing.mobile_number = director.mobile_number
                    existing.email = director.email
                    existing.pan_card_file = director.pan_card_file
                    existing.aadhaar_card_file = director.aadhaar_card_file
                    existing.bank_statement_file = director.bank_statement_file
                    existing.shareholding_percentage = director.shareholding_percentage
                    existing.residential_same_as_aadhaar_address = director.residential_same_as_aadhaar_address
                    existing.residential_address = director.residential_address
                    existing.residential_address_proof = director.residential_address_proof
                    existing.residential_address_proof_file = director.residential_address_proof_file
                    existing.save()

            except Shareholders.DoesNotExist:
                shareholder_details = Shareholders.objects.create(
                    service_request=instance.service_request,
                    service_task=instance.service_task,
                    status='in progress'
                )
                ShareholdersDetails.objects.create(
                    shareholders_ref=shareholder_details,
                    shareholder_first_name=director.director_first_name,
                    middle_name=director.middle_name,
                    last_name=director.last_name,
                    mobile_number=director.mobile_number,
                    email=director.email,
                    pan_card_file=director.pan_card_file,
                    aadhaar_card_file=director.aadhaar_card_file,
                    bank_statement_file=director.bank_statement_file,
                    shareholding_percentage=director.shareholding_percentage,
                    residential_same_as_aadhaar_address=director.residential_same_as_aadhaar_address,
                    residential_address=director.residential_address,
                    residential_address_proof=director.residential_address_proof,
                    residential_address_proof_file=director.residential_address_proof_file,
                    shareholder_type="Individual Indian Resident"
                )

    except DirectorsDetails.DoesNotExist:
        pass
    except Exception as e:
        print(f"Error in shareholder creation: {str(e)}")

@receiver(post_save, sender=Shareholders)
def sync_shareholders_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()


@receiver(post_save, sender=ReviewFilingCertificate)
def sync_review_service_task_status(sender, instance, **kwargs):
    task = instance.service_task

    # Sync status
    if task.status != instance.status:
        task.status = instance.status

    # Sync completion %
    task.completion_percentage = calculate_completion_percentage(instance)

    task.save()