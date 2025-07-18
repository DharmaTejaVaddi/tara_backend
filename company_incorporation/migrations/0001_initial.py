# Generated by Django 5.0.4 on 2025-06-26 14:54

import company_incorporation.helpers
import django.db.models.deletion
import usermanagement.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('servicetasks', '0001_initial'),
        ('usermanagement', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorizedPaidUpShareCapital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('authorized_share_capital', models.IntegerField(null=True)),
                ('paid_up_share_capital', models.IntegerField(null=True)),
                ('face_value_per_share', models.FloatField(null=True)),
                ('no_of_shares', models.PositiveIntegerField()),
                ('bank_name', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default='in progress', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorized_capital_assignee', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authorized_capital_reviewer', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='authorized_capital_service_request', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_task_authorized_capital', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='Directors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default='in progress', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_directors_details', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_directors_details', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='directors_details', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_task_directors_details', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='DirectorsDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('director_first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('category_of_directorship', models.CharField(blank=True, choices=[('Executive Director', 'executive director'), ('Non-Executive Director', 'non-executive director'), ('Independent Director', 'independent director'), ('Nominee Director', 'nominee director'), ('Managing Director', 'managing director'), ('Whole Time Director', 'whole time director'), ('Alternate Director', 'alternate director'), ('Additional Director', 'additional director'), ('Small Shareholder Director', 'small shareholder director'), ('Chairman And Managing Director', 'chairman and managing director'), ('Professional Director', 'professional director'), ('Government Nominee Director', 'government nominee director'), ('Foreign National Director', 'foreign national director'), ('Resident Director', 'resident director'), ('Non-Resident Director', 'non-resident director'), ('Woman Director', 'woman director'), ('Other', 'other')], max_length=100, null=True)),
                ('pan_card_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_pan_card_file)),
                ('aadhaar_card_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_aadhaar_card_file)),
                ('passport_photo_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_passport_photo_file)),
                ('mobile_number', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('father_first_name', models.CharField(max_length=50)),
                ('father_middle_name', models.CharField(blank=True, max_length=50)),
                ('father_last_name', models.CharField(max_length=50)),
                ('nationality', models.CharField(blank=True, choices=[('Indian', 'Indian'), ('Foreign National', 'Foreign National')], max_length=30, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('area_of_occupation', models.CharField(blank=True, max_length=30, null=True)),
                ('qualification', models.CharField(blank=True, choices=[('Below SSC', 'Below SSC'), ('SSC/Matriculation', 'SSC/Matriculation'), ('HSC/Intermediate/12th passed', 'HSC/Intermediate/12th passed'), ('Graduate', 'Graduate'), ('Post Graduate', 'Post Graduate'), ('Doctorate', 'Doctorate'), ('Professional Degree', 'Professional Degree'), ('Other', 'Other')], max_length=30, null=True)),
                ('residential_same_as_aadhaar_address', models.BooleanField(blank=True, default=False, help_text='Is the residential address same as Aadhaar address?', null=True)),
                ('residential_address', models.JSONField(blank=True, default=dict, null=True)),
                ('residential_address_proof', models.CharField(blank=True, choices=[('Bank Statement', 'Bank Statement'), ('Utility Bill', 'Utility Bill'), ('Telephone/Mobile Bill', 'Telephone/Mobile Bill'), ('Electricity Bill', 'Electricity Bill'), ('Property Tax Receipt', 'Property Tax Receipt'), ('Lease/Rent Agreement', 'Lease/Rent Agreement')], max_length=50, null=True)),
                ('residential_address_proof_file', models.FileField(blank=True, null=True, upload_to=company_incorporation.helpers.upload_residential_address_proof_file)),
                ('din_number', models.BooleanField(blank=True, default=False, help_text='Does the director have a Director Identification Number (DIN)?', null=True)),
                ('din_number_value', models.CharField(blank=True, max_length=30, null=True)),
                ('dsc', models.BooleanField(default=False, help_text='Does the director have a Digital Signature Certificate (DSC)?')),
                ('authorised_signatory_name', models.CharField(blank=True, max_length=100, null=True)),
                ('details_of_existing_directorships', models.BooleanField(blank=True, default=False, help_text='Does the director have any existing directorships?', null=True)),
                ('existing_directorships_details', models.JSONField(blank=True, default=list, null=True)),
                ('form_dir2', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_form_dir2)),
                ('is_this_director_also_shareholder', models.BooleanField(blank=True, default=False, help_text='Is this director also a shareholder?', null=True)),
                ('no_of_shares', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('shareholding_percentage', models.FloatField(null=True)),
                ('paid_up_capital', models.IntegerField(null=True)),
                ('specimen_signature_of_director', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_specimen_signature_of_director)),
                ('directors_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='directors', to='company_incorporation.directors')),
            ],
        ),
        migrations.CreateModel(
            name='ProposedCompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('proposed_company_names', models.JSONField(blank=True, default=dict, null=True)),
                ('objectives_of_company', models.TextField(blank=True, null=True)),
                ('business_activity', models.CharField(blank=True, choices=[('Agriculture', 'agriculture'), ('Forestry', 'forestry'), ('Fishing', 'fishing'), ('Mining And Quarrying', 'mining and quarrying'), ('Construction', 'construction'), ('Manufacturing', 'Manufacturing'), ('Education', 'education'), ('Finance', 'finance'), ('Art And Entertainment', 'art and entertainment'), ('Healthcare', 'healthcare'), ('Social Work', 'social work'), ('Transport And Logistics', 'transport and logistics'), ('Electricity', 'electricity'), ('Gas Supply', 'gas supply'), ('Steam', 'steam'), ('Water Supply', 'water supply'), ('Waste Management', 'waste management'), ('Rental And Leasing Services', 'rental and leasing services'), ('Hotel And Restaurant', 'hotel and restaurant'), ('Information And Communication', 'information and communication'), ('Wholesale And Retail Trade', 'wholesale and retail trade'), ('Accommodation And Food Services', 'accommodation and food services'), ('Support Services', 'support services'), ('Real Estate', 'real estate'), ('Financial Services', 'financial services'), ('Fund Management', 'fund management'), ('Financial And Insurance Activities', 'financial and insurance activities'), ('Management Consultancy', 'management consultancy'), ('Legal And Accounting', 'legal and accounting'), ('Business And Management Consultancy', 'business and management consultancy'), ('Other', 'Other')], max_length=255, null=True)),
                ('nic_code', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.BigIntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default='in progress', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_proposed_company_details', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_proposed_company_details', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='proposed_company_details', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_task_proposed_company_details', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='RegisteredOfficeAddressDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('ownership_type', models.CharField(blank=True, choices=[('Owned', 'Owned'), ('Rented', 'Rented'), ('Leased', 'Leased')], max_length=255, null=True)),
                ('proposed_office_address', models.JSONField(blank=True, default=dict, null=True)),
                ('utility_bill_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_utility_bill_file)),
                ('NOC_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_noc_file)),
                ('rent_agreement_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_rent_agreement_file)),
                ('property_tax_receipt_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_property_tax_receipt_file)),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default='in progress', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_registered_office_address_details', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_registered_office_address_details', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='registered_office_address', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_task_registered_office_address', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='ReviewFilingCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('review_certificate', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.review_filing_certificate)),
                ('draft_filing_certificate', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.draft_filing_certificate)),
                ('review_certificate_status', models.CharField(blank=True, choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default=None, max_length=20, null=True)),
                ('status', models.CharField(blank=True, choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], max_length=20, null=True)),
                ('filing_status', models.CharField(blank=True, choices=[('in progress', 'In Progress'), ('filed', 'Filed'), ('sent for approval', 'Sent for Approval'), ('resubmitted', 'Resubmitted')], default=None, max_length=20, null=True)),
                ('approval_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('resubmission', 'Resubmission'), ('sent for approval', 'Sent for Approval'), ('rejected', 'Rejected'), ('approved', 'Approved')], default=None, max_length=20, null=True)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_incorporation_review_filing_certificate', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_incorporation_review_filing_certificate', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_service_request_review_certificate', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_service_task_review_certificate', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='Shareholders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(default='Company Incorporation', editable=False, max_length=50)),
                ('status', models.CharField(choices=[('in progress', 'In Progress'), ('completed', 'Completed'), ('sent for approval', 'Sent for Approval'), ('revoked', 'Revoked')], default='in progress', max_length=20)),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_shareholders_details', to=settings.AUTH_USER_MODEL)),
                ('reviewer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reviewed_shareholders_details', to=settings.AUTH_USER_MODEL)),
                ('service_request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shareholders_details', to='usermanagement.servicerequest')),
                ('service_task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='service_task_shareholders_details', to='servicetasks.servicetask')),
            ],
        ),
        migrations.CreateModel(
            name='ShareholdersDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shareholder_first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(max_length=50)),
                ('shareholder_type', models.CharField(blank=True, choices=[('Individual Indian Resident', 'individual indian resident'), ('Individual Non-Resident', 'individual non-resident'), ('Individual Foreign National', 'individual foreign national'), ('Body Corporate Indian Company', 'body corporate indian company'), ('Body Corporate Foreign Company', 'body corporate foreign company'), ('Limited Liability Partnership', 'limited liability partnership')], max_length=50, null=True)),
                ('mobile_number', models.BigIntegerField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('pan_card_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_pan_card_file_shareholders)),
                ('aadhaar_card_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_aadhaar_card_file_shareholders)),
                ('bank_statement_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_bank_statement_file)),
                ('shareholding_percentage', models.FloatField(null=True)),
                ('residential_same_as_aadhaar_address', models.BooleanField(blank=True, default=False, help_text='Is the residential address same as Aadhaar address?', null=True)),
                ('residential_address', models.JSONField(blank=True, default=dict, null=True)),
                ('residential_address_proof', models.CharField(blank=True, choices=[('Bank Statement', 'Bank Statement'), ('Utility Bill', 'Utility Bill'), ('Telephone/Mobile Bill', 'Telephone/Mobile Bill'), ('Electricity Bill', 'Electricity Bill'), ('Property Tax Receipt', 'Property Tax Receipt'), ('Lease/Rent Agreement', 'Lease/Rent Agreement')], max_length=50, null=True)),
                ('residential_address_proof_file', models.FileField(blank=True, null=True, storage=usermanagement.models.PrivateS3Storage(), upload_to=company_incorporation.helpers.upload_address_proof_file_shareholder)),
                ('shareholders_ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shareholders', to='company_incorporation.shareholders')),
            ],
        ),
    ]
