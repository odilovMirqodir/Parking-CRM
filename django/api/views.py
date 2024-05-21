from rest_framework import generics
from my_app.models import Category, CategoryRegion, Auto, Parking
from .serializers import CategorySerializer, CategoryRegionSerializer, AutoSerializer, ParkingSerializer
from rest_framework.response import Response


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'category_name'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        data['regions'] = instance.categoryregion_set.values('id', 'car_count', 'region')
        data['autos'] = instance.categoryregion_set.values('auto__id', 'auto__parking_number', 'auto__car_id')

        return Response(data)


class CategoryRegionListCreateAPIView(generics.ListCreateAPIView):
    queryset = CategoryRegion.objects.all()
    serializer_class = CategoryRegionSerializer


class CategoryRegionDetailAPIView(generics.RetrieveAPIView):
    queryset = CategoryRegion.objects.all()
    serializer_class = CategoryRegionSerializer
    lookup_field = 'region'

    def retrieve(self, request, *args, **kwargs):
        region = self.get_object()
        category = region.category

        autos = Auto.objects.filter(category=region)

        category_serializer = CategorySerializer(category)
        region_serializer = self.get_serializer(region)
        autos_serializer = AutoSerializer(autos, many=True)

        response_data = {
            'category': category_serializer.data,
            'region': region_serializer.data,
            'autos': autos_serializer.data
        }

        return Response(response_data)


class AutoListCreateAPIView(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer


class AutoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    lookup_field = 'car_id'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = serializer.data
        if instance.category:
            data['category'] = instance.category.region
            data['category_region'] = instance.category.category.category_name
        else:
            data['category'] = None
            data['category_region'] = None

        return Response(data)


class ParkingCreateAPIView(generics.ListCreateAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer


class ParkingDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    lookup_field = 'parking_count'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        related_autos = instance.autos.all()

        related_autos_data = AutoSerializer(related_autos, many=True).data

        data = serializer.data
        data['related_autos'] = related_autos_data

        return Response(data)
