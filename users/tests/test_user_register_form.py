from unittest import TestCase
from django.urls import reverse
from users.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from parameterized import parameterized
from django.contrib.auth.models import User


class UserRegisterFormTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex: João'),
        ('last_name', 'Ex: Silva'),
        ('username', 'Ex: joao123'),
        ('email', 'Ex: joao123@gmail.com'),
        ('password', 'Ex: João@123'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_placeholder_is_correct(self, field_name, placeholder):
        form = RegisterForm()
        self.assertEqual(
            form.fields[field_name].widget.attrs['placeholder'], placeholder)

    @parameterized.expand([
        ('username', (
            "O usuário deve conter apenas letras, números e @/./+/-/_."
            "O tamanho deve estar entre 4 e 150 caracteres."
        )),
        ('password', (
            "A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números."
        ))
    ])
    def test_help_text_is_correct(self, field_name, help_text):
        form = RegisterForm()
        self.assertEqual(
            form.fields[field_name].help_text, help_text)

    @parameterized.expand([
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Nome de usuário'),
        ('email', 'Endereço de email'),
        ('password', 'Senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_label_is_correct(self, field_name, label):
        form = RegisterForm()
        self.assertEqual(
            form.fields[field_name].label, label)


class UserRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.user = User.objects.create_user(
            username='joao123', password='João@123', email='joao123@gmail.com')
        self.client.login(username='joao123', password='João@123')
        self.form_data = {
            'first_name': 'João',
            'last_name': 'Silva',
            'username': 'joao123',
            'email': 'joao123@gmail.com',
            'password': 'João@123',
            'password2': 'João@123',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
        ('first_name', 'O primeiro nome é obrigatório.'),
        ('last_name', 'O sobrenome é obrigatório.'),
        ('email', 'O e-mail é obrigatório.'),
        ('password', 'A senha é obrigatória.'),
        ('password2', 'A confirmação da senha é obrigatória.'),

    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_min_lenght_should_be_4(self):
        self.form_data['username'] = 'jo'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'O tamanho mínimo é 4 caracteres.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_max_lenght_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'O tamanho máximo é 150 caracteres.'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'Kaique'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'A senha deve conter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas e números.'
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Kaique123'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(response.context['form'].errors.get('password'), None)

    def test_passwords_must_match(self):
        self.form_data['password'] = 'Kaique123'
        self.form_data['password2'] = 'Kaique1234'
        url = reverse('users:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'As senhas não coincidem.'
        self.assertIn(msg, response.context['form'].errors.get('password2'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'Kaique123'
        self.form_data['password2'] = 'Kaique123'
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertEqual(
            response.context['form'].errors.get('password2'), None)

    def test_send_get_request_return_404(self):
        url = reverse('users:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_username_already_exists(self):
        url = reverse('users:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        msg = 'Esse nome de usuário já está em uso.'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_email_already_exists(self):
        url = reverse('users:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        msg = 'Esse e-mail já está em uso.'

        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_user_created_can_login(self):
        url = reverse('users:register_create')
        self.form_data.update({
            'username': 'teste',
            'email': 'teste@teste.com',
            'password': '@Abc123456',
            'password2': '@Abc123456',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='teste',
            password='@Abc123456'
        )

        self.assertTrue(is_authenticated)
