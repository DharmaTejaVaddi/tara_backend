from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
import json
from .models import *
from .serializers import *


# BasicBusinessInfo Views
@api_view(['POST', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def basic_business_info_list_create(request):
    try:
        if request.method == 'POST':
            serializer = BasicBusinessInfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            objs = BasicBusinessInfo.objects.all()
            serializer = BasicBusinessInfoSerializer(objs)
            return Response(serializer.data)
        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def basic_business_info_by_service_request(request):
    try:
        service_request_id = request.query_params.get('service_request_id')
        if not service_request_id:
            return Response(
                {"error": "Provide 'service_request_id' as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )

        instance = BasicBusinessInfo.objects.get(service_request_id=service_request_id)
        serializer = BasicBusinessInfoSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except BasicBusinessInfo.DoesNotExist:
        return Response({"error": "Basic Business Info not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def basic_business_info_detail(request, pk):
    try:
        basic_business_info = BasicBusinessInfo.objects.get(pk=pk)
    except BasicBusinessInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = BasicBusinessInfoSerializer(basic_business_info)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = BasicBusinessInfoSerializer(basic_business_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            file_to_delete = request.query_params.get('file')
            if file_to_delete: # If a specific file is requested for deletion
                if file_to_delete == 'business_pan' and basic_business_info.business_pan:
                    basic_business_info.business_pan.storage.delete(
                        basic_business_info.business_pan.name)
                    basic_business_info.business_pan = None
                elif (file_to_delete == 'certificate_of_incorporation' and
                      basic_business_info.certificate_of_incorporation):
                    basic_business_info.certificate_of_incorporation.storage.delete(
                        basic_business_info.certificate_of_incorporation.name)
                    basic_business_info.certificate_of_incorporation = None
                elif file_to_delete == 'MOA_AOA' and basic_business_info.MOA_AOA:
                    basic_business_info.MOA_AOA.storage.delete(
                        basic_business_info.MOA_AOA.name)
                    basic_business_info.MOA_AOA = None
                else:
                    return Response({"error": "Invalid or missing file name"}, status=status.HTTP_400_BAD_REQUEST)
                basic_business_info.save()
                return Response({"message": f"{file_to_delete} deleted successfully"}, status=status.HTTP_200_OK)

            # If need to delete entire object and its files
            if basic_business_info.business_pan:
                basic_business_info.business_pan.storage.delete(basic_business_info.business_pan.name)
            if basic_business_info.certificate_of_incorporation:
                basic_business_info.certificate_of_incorporation.storage.delete(
                    basic_business_info.certificate_of_incorporation.name)
            if basic_business_info.MOA_AOA:
                basic_business_info.MOA_AOA.storage.delete(basic_business_info.MOA_AOA.name)
            basic_business_info.delete()
            return Response({"message": "Basic Business Info details deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# RegistrationInfo Views
@api_view(['POST', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def registration_info_list_create(request):
    try:
        if request.method == 'POST':
            serializer = RegistrationInfoSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            objs = RegistrationInfo.objects.all()
            serializer = RegistrationInfoSerializer(objs)
            return Response(serializer.data)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def registration_info_by_service_request(request):
    try:
        service_request_id = request.query_params.get('service_request_id')

        if not service_request_id:
            return Response({"error": "Provide 'service_request_id' as a query parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        instance = RegistrationInfo.objects.get(service_request_id=service_request_id)
        serializer = RegistrationInfoSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except RegistrationInfo.DoesNotExist:
        return Response({"error": "Registration Info not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def registration_info_detail(request, pk):
    try:
        registrations_info = RegistrationInfo.objects.get(pk=pk)
    except RegistrationInfo.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = RegistrationInfoSerializer(registrations_info)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = RegistrationInfoSerializer(registrations_info, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            registrations_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# PrincipalPlaceDetails Views
@api_view(['POST', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def principal_place_details_list_create(request):
    try:
        if request.method == 'POST':
            data = dict(request.data)
            for key in data:
                if isinstance(data[key], list) and len(data[key]) == 1:
                    data[key] = data[key][0]
            val = data.get('principal_place')
            if val:
                if isinstance(val, str):
                    try:
                        data['principal_place'] = json.loads(val)
                    except json.JSONDecodeError:
                        return Response({"principal_place": ["Value must be valid JSON."]},
                                        status=status.HTTP_400_BAD_REQUEST)
                elif not isinstance(val, dict):
                    return Response({"principal_place": ["Value must be a JSON object or string."]},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = PrincipalPlaceDetailsSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            objs = PrincipalPlaceDetails.objects.all()
            serializer = PrincipalPlaceDetailsSerializer(objs)
            return Response(serializer.data)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def principal_place_details_by_service_request(request):
    try:
        service_request_id = request.query_params.get('service_request_id')
        if not service_request_id:
            return Response({"error": "Missing service_request_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = PrincipalPlaceDetails.objects.get(service_request_id=service_request_id)
        except PrincipalPlaceDetails.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PrincipalPlaceDetailsSerializer(obj)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def principal_place_details_detail(request, pk):
    try:
        principal_place_details = PrincipalPlaceDetails.objects.get(pk=pk)
    except PrincipalPlaceDetails.DoesNotExist:
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = PrincipalPlaceDetailsSerializer(principal_place_details)
            return Response(serializer.data)

        elif request.method == 'PUT':
            data = request.data.copy()
            principal_place = data.get('principal_place')
            if principal_place and isinstance(principal_place, str):
                try:
                    principal_place = json.dumps(json.loads(principal_place))
                    data['principal_place'] = principal_place
                except json.JSONDecodeError:
                    return Response({"principal_place": ["Value must be valid JSON."]},
                                    status=status.HTTP_400_BAD_REQUEST)

            serializer = PrincipalPlaceDetailsSerializer(principal_place_details, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            file_to_delete = request.query_params.get('file')
            if file_to_delete: # If a specific file is requested for deletion
                if file_to_delete == 'address_proof_file' and principal_place_details.address_proof_file:
                    principal_place_details.address_proof_file.storage.delete(
                        principal_place_details.address_proof_file.name)
                    principal_place_details.address_proof_file = None
                elif file_to_delete == 'rental_agreement_or_noc' and principal_place_details.rental_agreement_or_noc:
                    principal_place_details.rental_agreement_or_noc.storage.delete(
                        principal_place_details.rental_agreement_or_noc.name)
                    principal_place_details.rental_agreement_or_noc = None
                elif (file_to_delete == 'bank_statement_or_cancelled_cheque' and
                      principal_place_details.bank_statement_or_cancelled_cheque):
                    principal_place_details.bank_statement_or_cancelled_cheque.storage.delete(
                        principal_place_details.bank_statement_or_cancelled_cheque.name)
                    principal_place_details.bank_statement_or_cancelled_cheque = None
                else:
                    return Response({"error": "Invalid or missing file name"}, status=status.HTTP_400_BAD_REQUEST)
                principal_place_details.save()
                return Response({"message": f"{file_to_delete} deleted successfully"}, status=status.HTTP_200_OK)

            # If need to delete entire object and its files
            if principal_place_details.address_proof_file:
                principal_place_details.address_proof_file.storage.delete(
                    principal_place_details.address_proof_file.name)

            if principal_place_details.rental_agreement_or_noc:
                principal_place_details.rental_agreement_or_noc.storage.delete(
                    principal_place_details.rental_agreement_or_noc.name)

            if principal_place_details.bank_statement_or_cancelled_cheque:
                principal_place_details.bank_statement_or_cancelled_cheque.storage.delete(
                    principal_place_details.bank_statement_or_cancelled_cheque.name)

            principal_place_details.delete()

            return Response({"message": "Principal place details deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Promoter Signatory Details Views
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def upsert_promoter_signatory_data(request):
    data = request.data
    service_request_id = data.get('service_request')

    if not service_request_id:
        return Response({"error": "Missing service_request"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        promoter_details_payload = {
            "service_request": service_request_id,
            "service_task": data.get("service_task"),
            "status": data.get("status"),
            "assignee": data.get("assignee"),
            "reviewer": data.get("reviewer")
        }
        # Upsert PromoterSignatoryDetails
        try:
            details_instance = PromoterSignatoryDetails.objects.get(service_request_id=service_request_id)
            details_serializer = PromoterSignatoryDetailsSerializer(details_instance, data=promoter_details_payload,
                                                                    partial=True)
        except PromoterSignatoryDetails.DoesNotExist:
            details_serializer = PromoterSignatoryDetailsSerializer(data=promoter_details_payload)

        if not details_serializer.is_valid():
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        details_instance = details_serializer.save()
        promoter_info_id = data.get("id")
        data["promoter_detail"] = details_instance.id

        # Combine form data and files explicitly for info serializer
        if promoter_info_id:
            try:
                info_instance = PromoterSignatoryInfo.objects.get(pk=promoter_info_id, promoter_detail=details_instance)
                info_serializer = PromoterSignatoryInfoSerializer(
                    instance=info_instance,
                    data=data,
                    partial=True
                )
            except PromoterSignatoryInfo.DoesNotExist:
                info_serializer = PromoterSignatoryInfoSerializer(data=data)
        else:
            info_serializer = PromoterSignatoryInfoSerializer(data=data)

        if not info_serializer.is_valid():
            if not promoter_info_id:
                details_instance.delete()
            return Response(info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        info_instance = info_serializer.save()

        return Response({
            "message": "PromoterSignatoryDetails and Info saved successfully",
            "details": PromoterSignatoryDetailsSerializer(details_instance).data,
            "info": PromoterSignatoryInfoSerializer(info_instance).data
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_promoter_signatory_data(request):
    service_request_id = request.query_params.get('service_request_id')
    if not service_request_id:
        return Response({"error": "Missing service_request"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        details = PromoterSignatoryDetails.objects.get(service_request_id=service_request_id)
    except PromoterSignatoryDetails.DoesNotExist:
        return Response({"error": "PromoterSignatoryDetails not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        info = PromoterSignatoryInfo.objects.get(promoter_detail=details)
        info_data = PromoterSignatoryInfoSerializer(info).data
    except PromoterSignatoryInfo.DoesNotExist:
        info_data = None

    return Response({
        "details": PromoterSignatoryDetailsSerializer(details).data,
        "info": info_data
    }, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def promoter_signatory_info_delete(request, pk):
    try:
        info = PromoterSignatoryInfo.objects.get(pk=pk)
    except PromoterSignatoryInfo.DoesNotExist:
        return Response({"error": "Promoter Signatory Info not found"}, status=status.HTTP_404_NOT_FOUND)

    try:
        file_to_delete = request.query_params.get('file')
        if file_to_delete:
            if file_to_delete == 'pan' and info.pan:
                info.pan.storage.delete(info.pan.name)
                info.pan = None
            elif file_to_delete == 'aadhaar' and info.aadhaar:
                info.aadhaar.storage.delete(info.aadhaar.name)
                info.aadhaar = None
            elif file_to_delete == 'photo' and info.photo:
                info.photo.storage.delete(info.photo.name)
                info.photo = None
            else:
                return Response({"error": "Invalid or missing file name"}, status=status.HTTP_400_BAD_REQUEST)

            info.save()
            return Response({"message": f"{file_to_delete} deleted successfully"}, status=status.HTTP_200_OK)

        if info.pan:
            info.pan.storage.delete(info.pan.name)
        if info.aadhaar:
            info.aadhaar.storage.delete(info.aadhaar.name)
        if info.photo:
            info.photo.storage.delete(info.photo.name)

        info.delete()
        return Response({"message": "Promoter Signatory Info and all associated files deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# GSTReviewFilingCertificate Views
@api_view(['POST', 'GET'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def gst_review_filing_certificate_list_create(request):
    try:
        if request.method == 'POST':
            serializer = GSTReviewFilingCertificateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            objs = GSTReviewFilingCertificate.objects.all()
            serializer = GSTReviewFilingCertificateSerializer(objs, many=True)
            return Response(serializer.data)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def gst_review_filing_certificate_by_service_request(request):
    try:
        service_request_id = request.query_params.get('service_request_id')
        if not service_request_id:
            return Response({"error": "Missing service_request_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obj = GSTReviewFilingCertificate.objects.get(service_request_id=service_request_id)
        except GSTReviewFilingCertificate.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GSTReviewFilingCertificateSerializer(obj)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def gst_review_filing_certificate_detail(request, pk):
    try:
        gst_certificate = GSTReviewFilingCertificate.objects.get(pk=pk)
    except GSTReviewFilingCertificate.DoesNotExist:
        return Response({"error": "Not found"},  status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer = GSTReviewFilingCertificateSerializer(gst_certificate)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = GSTReviewFilingCertificateSerializer(gst_certificate, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if gst_certificate.review_certificate:
                gst_certificate.review_certificate.storage.delete(
                    gst_certificate.review_certificate.name)
            gst_certificate.delete()
            return Response({"message": "GST Review Filing Certificate deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)

        return Response({"error": "Invalid request method"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
