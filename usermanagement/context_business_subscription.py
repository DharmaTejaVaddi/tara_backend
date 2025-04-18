from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import logging

from models import (
    Users, Context, Role, UserContextRole, Module,
    ModuleFeature, UserFeaturePermission, SubscriptionPlan, ModuleSubscription, Business
)

# Configure logging
logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_business_context(request):
    """
    Create a new business context without a subscription plan.

    Expected request data:
    {
        "user_id": 1,
        "business_name": "My Business",
        "registration_number": "REG123",
        "entity_type": "privateLimitedCompany",
        "head_office": {
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "country": "USA",
            "pincode": "10001"
        },
        "pan": "ABCDE1234F",
        "business_nature": "Technology",
        "trade_name": "MyTrade",
        "mobile_number": "+1234567890",
        "email": "business@example.com",
        "dob_or_incorp_date": "2020-01-01"
    }
    """
    # Extract data from request
    user_id = request.data.get('user_id')
    business_name = request.data.get('business_name')
    # Extract additional business data
    registration_number = request.data.get('registration_number')
    entity_type = request.data.get('entity_type')
    head_office = request.data.get('head_office')
    pan = request.data.get('pan')
    business_nature = request.data.get('business_nature')
    trade_name = request.data.get('trade_name')
    mobile_number = request.data.get('mobile_number')
    email = request.data.get('email')
    dob_or_incorp_date = request.data.get('dob_or_incorp_date')

    # Validate required fields
    if not all([user_id, business_name]):
        return Response(
            {"error": "Missing required fields. Please provide user_id and business_name."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            # Get user
            try:
                user = Users.objects.get(id=user_id)
            except Users.DoesNotExist:
                return Response(
                    {"error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Check if user is active
            if user.is_active != 'yes':
                return Response(
                    {"error": "User account is not active. Please activate your account first."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Create business context
            context = Context.objects.create(
                name=business_name,
                context_type='business',
                owner_user=user,
                status='active',
                profile_status='complete'
            )

            # Create owner role for the business
            owner_role = Role.objects.get(
                context=context,
                role_type='owner'
            )

            # Assign user to context with owner role
            user_context_role = UserContextRole.objects.create(
                user=user,
                context=context,
                role=owner_role,
                status='active',
                added_by=user
            )

            # Create business record with additional data
            business = Business.objects.create(
                client=user,
                nameOfBusiness=business_name,
                registrationNumber=registration_number,
                entityType=entity_type,
                headOffice=head_office,
                pan=pan,
                business_nature=business_nature,
                trade_name=trade_name,
                mobile_number=mobile_number,
                email=email,
                dob_or_incorp_date=dob_or_incorp_date
            )

            return Response({
                "message": "Business context created successfully",
                "context_id": context.id,
                "business_id": business.id,
                "business_name": business_name
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error creating business context: {str(e)}")
        return Response(
            {"error": f"An error occurred while creating the business context: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def add_subscription_to_business(request):
    """
    Add a subscription plan to an existing business context.

    Expected request data:
    {
        "context_id": 1,
        "module_id": 1,
        "subscription_plan_id": 1
    }
    """
    # Extract data from request
    context_id = request.data.get('context_id')
    module_id = request.data.get('module_id')
    subscription_plan_id = request.data.get('subscription_plan_id')

    # Validate required fields
    if not all([context_id, module_id, subscription_plan_id]):
        return Response(
            {"error": "Missing required fields. Please provide context_id, module_id, and subscription_plan_id."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        with transaction.atomic():
            # Get context
            try:
                context = Context.objects.get(id=context_id, context_type='business')
            except Context.DoesNotExist:
                return Response(
                    {"error": "Business context not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get module
            try:
                module = Module.objects.get(id=module_id)
            except Module.DoesNotExist:
                return Response(
                    {"error": "Module not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get subscription plan
            try:
                subscription_plan = SubscriptionPlan.objects.get(id=subscription_plan_id)
            except SubscriptionPlan.DoesNotExist:
                return Response(
                    {"error": "Subscription plan not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Create module subscription
            module_subscription = ModuleSubscription.objects.create(
                context=context,
                module=module,
                plan=subscription_plan,
                status='active',
                start_date=timezone.now(),
                end_date=timezone.now() + relativedelta(days=subscription_plan.billing_cycle_days),
                auto_renew=False
            )

            # Get all features for the module
            module_features = ModuleFeature.objects.filter(module=module)

            # Create feature permissions for all users in the context
            user_context_roles = UserContextRole.objects.filter(context=context)
            for ucr in user_context_roles:
                # Collect all unique service.action combinations
                all_actions = []
                for feature in module_features:
                    action = f"{feature.service}.{feature.action}"
                    if action not in all_actions:
                        all_actions.append(action)

                # Create a single user feature permission with all actions
                UserFeaturePermission.objects.create(
                    user_context_role=ucr,
                    module=module,
                    actions=all_actions,
                    is_active='yes',
                    created_by=context.owner_user
                )

            return Response({
                "message": "Subscription added successfully",
                "module_subscription_id": module_subscription.id,
                "start_date": module_subscription.start_date,
                "end_date": module_subscription.end_date
            }, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Error adding subscription to business: {str(e)}")
        return Response(
            {"error": f"An error occurred while adding the subscription: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

