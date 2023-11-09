from rest_framework import generics,mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from .models import Product
from .serializers import ProductSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON

    def perform_create(self, serializer):
        # You can add custom logic here before saving the object.
        # For example, you can set default values or perform additional validations.
        # Get the title from the validated data and convert it to uppercase
        title = serializer.validated_data.get('title', '').upper()
        # The second argument '' is a default value that will be returned if the key ('title') is not found in the dictionary.
        # Update the title in the data before saving
        serializer.validated_data['title'] = title
        # Call the parent class's perform_create method to save the object
        super().perform_create(serializer)
        # or
        # serializer.save()
    
product_create_view=ProductCreateAPIView.as_view()

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON

product_detail_view=ProductDetailAPIView.as_view()


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON

product_list_view=ProductListAPIView.as_view()


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON
    
product_list_create_view=ProductListCreateAPIView.as_view()


class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON
    lookup_field = 'pk'
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = 'Content Not Provided'
        # return super().perform_update(serializer)
product_update_view=ProductUpdateAPIView.as_view()



class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()  # Specify the queryset to retrieve objects from
    serializer_class = ProductSerializer  # Specify the serializer to convert model instances to JSON
    
product_destroy_view=ProductDestroyAPIView.as_view()





# mixins combined with generics approach (we want to learn its not our route)
# when we use mixins, we get the access to use some methods that are built into the mixin 
# like here when the method is get (get(self.....)) it returns self.list that is a method that return list of all products, we can do 
# also post() and return self.list, it's so flexible !

## mixin that do the same as ProductListAPIView
# class ProductMixinView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = Product.objects.all()  
#     serializer_class = ProductSerializer  

#     def get(self, request, *args, **kwargs): 
#         return self.list(request, **args, **kwargs)
    
# product_mixin_view = ProductMixinView.as_view()

# class ProductMixinView(mixins.ListModelMixin,generics.GenericAPIView):
#     queryset = Product.objects.all()  
#     serializer_class = ProductSerializer  

#     def get(self, request, *args, **kwargs): 
#         return self.list(request, **args, **kwargs)
    
# product_mixin_view = ProductMixinView.as_view()


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # this lookup_field is a must to let RetriveModelMixin work 
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get
        # print(args, kwargs) this line print (<>, {'pk' : '3'}) so we want to get the pk that we want to lookup with 
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    # The perform_create method is a hook provided by Django REST Framework 
    # that allows you to customize the creation of a new object during the POST request 
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

    # def post(): #HTTP -> post

product_mixin_view = ProductMixinView.as_view()




# custom django view 
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method  

    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all() 
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)

















