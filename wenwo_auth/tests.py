from django.test import TestCase
from django.core.cache import cache

def test_redis(request):
    cache.set("name", "tom", 20) # 该值的有效期为20s
    print(cache.has_kay("name"))  # 包含: true
    print(cache.get("name"))  # 返回: tom  无返回null
