from celery import shared_task
from .models import UrlCheck, Test
import requests
from selenium import webdriver
from django.core.files.base import ContentFile
import os
import shutil
from django.conf import settings

@shared_task
def add(x, y):
    print(f'{x}+{y}= {x+y}')
    return x + y

@shared_task
def create_tests(id):
    num_of_test_spawned = 0
    # REQUEST
    url_check = UrlCheck.objects.get(pk=id)

    test = Test(test_type='request_http_get',
                url_check=url_check,
                status='QUEUED')
    test.save()
    url_test_request_get.delay(test.id)
    num_of_test_spawned += 1

    # SELENIUM
    test = Test(test_type='url_test_selenium',
                url_check=url_check,
                status='QUEUED')
    test.save()
    url_test_selenium.delay(test.id)
    num_of_test_spawned += 1
    return {'url_check': id, 'num_of_test_spawned': num_of_test_spawned}


@shared_task
def url_test_request_get(test_id):
    test = Test.objects.get(pk=test_id)
    test.status = 'IN-PROGRESS'
    test.save()

    try:
        request = requests.get(test.url_check.url)
    except Exception as e:
        test.result = False
        test.details = "Was not able to get to web server" + str(e)
        test.status = 'COMPLETED'
        test.save()
        return {'test': test_id, 'status': test.status}

    test.details = f'Was able to connect to webserver, status code: {request.status_code}'
    test.status = "COMPLETED"
    test.result = True
    test.save()

    return {'test': test_id, 'status': test.status}


@shared_task
def url_test_selenium(test_id):
    test = Test.objects.get(pk=test_id)
    test.status = 'IN-PROGRESS'
    test.save()

    # Create a headless browser instance
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=options)

    # Navigate to the website you want to screenshot
    url = test.url_check.url
    try:
        browser.get(url)

        # Take a screenshot and save it to a file
        screenshot_filename = f'{test_id}.png'
        browser.save_screenshot(screenshot_filename)

        # Close the browser instance
        browser.quit()
    except Exception as e:
        test.result = False
        test.details = "Was not able to get to web server" + str(e)
        test.status = 'COMPLETED'
        test.save()
        return {'test': test_id, 'status': test.status}
    test.details = f'Was able to connect to webpage'
    test.status = "COMPLETED"
    test.result = True

    if os.path.isfile(screenshot_filename):
        media_root = settings.MEDIA_ROOT
        file_name = os.path.basename(screenshot_filename)
        destination_path = os.path.join(media_root, file_name)
        shutil.copy2(screenshot_filename, destination_path)
        os.remove(screenshot_filename)
    test.proof_image = True
    test.save()
    return {'test': test_id, 'status': test.status}
