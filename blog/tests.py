from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

class TestView(TestCase):
    def setup(self):
        self.client = Client()

    def navbar_test(self,soup):
        navbar = soup.nav
        self.assertIn('국비 지원 기관 정보 사이트', navbar.text)
        self.assertIn('About Developer', navbar.text)

        logo_btn = navbar.find('a',text='국비 지원 기관 정보 사이트')
        self.assertEqual(logo_btn.attrs['href'],'/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Information')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_developer_btn = navbar.find('a', text='About Developer')
        self.assertEqual(about_developer_btn.attrs['href'], '/about_developer/')

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code,200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text,'국비 지원 기관 정보')
        self.navbar_test(soup)

        self.assertEqual(Post.objects.count(),0)
        main_area = soup.find('div',id='main_area')

        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world',
        )

        post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아님',
        )

        self.assertEqual(Post.objects.count(),2)

        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)
        main_area = soup.find('div',id='main-area')
        self.assertIn(post_001.title,main_area.text)
        self.assertIn(post_002.title,main_area.text)
        self.assertNotIn('아직 게시물이 없습니다.',main_area.text)

        def test_post_detail(self):
            post_001 = Post.objects.create(
                title='첫번째 포스트입니다.',
                content='Hello World. We are the world',
            )
            self.assertEqual(post_001.get_absolute_url(),'blog/1/')

            response = self.client.get(post_001.get_absolute_url())
            self.assertEqual(response.status_code,200)
            soup = BeautifulSoup(response.content,'html/parser')

            self.navbar_test(soup)

            self.assertIn(post_001.title,soup.title.text)

            main_area = soup.find('div',id='main-area')
            post_area = main_area.find('div',id='post-area')
            self.assertIn(post_001.title, post_area.text)

            self.assertIn(post_001.content,post_area.text)