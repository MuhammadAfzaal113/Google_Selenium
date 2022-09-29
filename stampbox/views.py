import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from helpers.log_util import logger
from rest_framework.permissions import AllowAny
from stampbox.serializer import image_Add_serializer
from stampbox.using_selenium import use_sel_model
import os
from djangoProject.config import Config
import shutil
# import cv2 as cv


env = Config.environment(mode_selection='development')


def remove_img(img_param):
    if os.path.exists(img_param):
        os.remove(img_param)
    else:
        print('File not deleted', img_param)


def sel_function(img):
    text_list = use_sel_model(img)
    if text_list:
        repeat = False
        status_code = status.HTTP_200_OK
        response = {
            'success': True,
            'status_code': status_code,
            'message': 'Image File added Successfully',
            # 'data': serializer.data,
            'extracted_details': text_list
        }
        remove_img(img)
        return response, status_code, repeat

    else:
        repeat = True
        status_code = status.HTTP_204_NO_CONTENT
        response = {
            'success': False,
            'status_code': status_code,
            'message': 'Unable to Apply OCR'
        }
        # remove_img(img)
        return response, status_code, repeat


class ClassificationView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = image_Add_serializer

    def get(self, request, *args, **kwargs):
        status_code = status.HTTP_200_OK
        response = {
            'status': status_code,
            'success': True,
            'message': 'GET API Working'
        }
        return Response(response, status_code)

    def post(self, request, *args, **kwargs):
        try:
            logger.info(f"User-Agent: {request.headers.get('User-Agent')}")
            logger.info('[METHOD: POST] [ClassificationView] Predicting text from image')

            if request.data['media_link']:

                text_list = use_sel_model(request.data['media_link'])
                if text_list:
                    status_code = status.HTTP_200_OK
                    response = {
                        'success': True,
                        'status_code': status_code,
                        'message': 'Image File added Successfully',
                        'extracted_details': text_list
                    }
                    return Response(response, status_code)

                else:
                    status_code = status.HTTP_204_NO_CONTENT
                    response = {
                        'success': False,
                        'status_code': status_code,
                        'message': 'Unable to Apply OCR'
                    }
                    return Response(response, status_code)

            else:
                response = {
                    'success': False,
                    'message': 'bad request image_link is required in request body'
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f'[METHOD: POST] [ClassificationView] exception occurred as {e}')
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'status_code': status_code,
                'success': False,
                'message': f'bad request {e}'
            }
            return Response(response, status_code)


def download_image(url, file_name):
    res = requests.get(url, stream=True)

    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Successful: ', file_name)
        return True
    else:
        print('Image Could not be retrieved')
        return False


# class MatchImages(APIView):
#     permission_classes = (AllowAny,)
#
#     def get(self, request, *args, **kwargs):
#         status_code = status.HTTP_200_OK
#         response = {
#             'status': status_code,
#             'success': True,
#             'message': 'Use Post request'
#         }
#         return Response(response, status_code)
#
#     def post(self, request):
#         try:
#             logger.info('[METHOD: POST] [MatchImages] Match Given Images')
#             old_image = request.data.get('old_image')
#             new_image = request.data.get('new_image')
#             base = cv.imread(old_image)
#             test = cv.imread(new_image)
#             hsv_base = cv.cvtColor(base, cv.COLOR_BGR2HSV)
#             hsv_test = cv.cvtColor(test, cv.COLOR_BGR2HSV)
#
#             h_bins = 50
#             s_bins = 60
#             histSize = [h_bins, s_bins]
#             h_ranges = [0, 180]
#             s_ranges = [0, 256]
#             ranges = h_ranges + s_ranges
#             channels = [0, 1]
#
#             hist_base = cv.calcHist([hsv_base], channels, None, histSize, ranges, accumulate=False)
#             cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
#             hist_test = cv.calcHist([hsv_test], channels, None, histSize, ranges, accumulate=False)
#             cv.normalize(hist_test, hist_test, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
#
#             compare_method = cv.HISTCMP_CORREL
#
#             base_base = cv.compareHist(hist_base, hist_base, compare_method)
#             base_test = cv.compareHist(hist_base, hist_test, compare_method)
#
#             response = {
#                 'success': True,
#                 'message': 'Score of matching images',
#                 'base_base': base_base,
#                 'base_test': base_test
#             }
#             return Response(response, status.HTTP_200_OK)
#
#         except Exception as e:
#             logger.error(f'[METHOD: POST] [MatchImages] throws exception {e}')
#             response = {
#                 'success': False,
#                 'message': f'bad request {e}'
#             }
#             return Response(response, status.HTTP_400_BAD_REQUEST)
