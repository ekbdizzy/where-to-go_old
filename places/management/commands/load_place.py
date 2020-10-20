from django.core.management.base import BaseCommand
from places.models import Place, PlacesImages
import requests
import logging
from utils import SaveImagePlace

logger = logging.getLogger('main')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'url',
            help='Create Place and ImagesPlace model with data from url'
        )

    def handle(self, *args, **options):
        url = options['url']
        response = requests.get(url)
        response.raise_for_status()

        response_data = response.json()
        try:
            title = response_data['title']
            imgs = response_data['imgs']
            short_description = response_data['description_short']
            detailed_description = response_data['description_long']
            longitude_coord = response_data['coordinates']['lng']
            latitude_coord = response_data['coordinates']['lat']
        except KeyError as e:
            logger.error(e)
            return

        place = Place.objects.get_or_create(
            title=title,
            short_description=short_description,
            detailed_description=detailed_description,
            longitude_coord=longitude_coord,
            latitude_coord=latitude_coord
        )

        print(place)

        # if place[1]:
        #     logger.info('{} is created'.format(place[0].title))
        #
        # for image_link in imgs:
        #     s = SaveImagePlace()
        #     s.save(image_link)
        #
        #     new_image_place = PlacesImages.objects.create(
        #         place=place[0],
        #         image=f"places/{image_link.split('/')[-1]}"
        #     )
        #     new_image_place.save()
