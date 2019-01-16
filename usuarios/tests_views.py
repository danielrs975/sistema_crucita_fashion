"""
Script que contiene las pruebas
para las vistas de esta aplicacion
"""
from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from usuarios.models import Usuario, Group, GRUPOS
from usuarios.serializers import RegistroSerializer
from usuarios import views

class LoginViewTest(APITestCase):
    """
    Clase que contiene las pruebas para
    la vista del login
    """
    def setUp(self):
        """
        Inicializa la base de datos con
        informacion para correr las pruebas
        """
        for grupo in GRUPOS:
            Group.objects.create(name=grupo)
        self.usuario_data = {
            "first_name": "Daniel",
            "last_name" : "Rodriguez",
            "username"  : "danielrs",
            "email"     : "danielrs9705@gmail.com",
            "password"  : "jaja123",
            "repeat_password": "jaja123",
            "grupo"     : Group.objects.get(name="Cliente").pk
        }
        registro_serializer = RegistroSerializer(data=self.usuario_data)
        registro_serializer.is_valid()
        registro_serializer.save()
        self.url = reverse_lazy("usuarios:login")

    def test_login_view(self): # pylint: disable=no-self-use
        """
        Prueba que la vista funcione correctamente
        """
        views.LoginView.as_view()

    def test_login_valido(self):
        """
        Prueba que la vista del login
        funcione con informacion valida
        """
        data = {"username": "danielrs", "password":"jaja123"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_login_invalido(self):
        """
        Prueba que si el usuario y el
        password es invalido no se puede loggear
        """
        data = {"username": "danielrs", "password": "jaja1234"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

class UsuarioRegistroView(APITestCase):
    """
    Clase que contiene las pruebas de la
    vista de registro
    """
    def setUp(self):
        """
        Metodo que llena la base de datos
        con informacion para correr las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.usuario_data = {
            "first_name": "Daniel",
            "last_name" : "Rodriguez",
            "email"     : "danielrs9705@gmail.com",
            "username"  : "danielrs",
            "grupo"     : self.grupos[3].pk,
            "password"  : "jaja123",
            "repeat_password": "jaja123"
        }
        self.usuario_data_2 = {
            "first_name": "Rafael",
            "last_name" : "Rodriguez",
            "email"     : "rafael@gmail.com",
            "username"  : "rafaelrs",
            "grupo"     : self.grupos[3].pk,
            "password"  : "jaja123",
            "repeat_password": "jaja123"
        }
        registro = RegistroSerializer(data=self.usuario_data_2)
        registro.is_valid()
        registro.save()
        self.url = reverse_lazy("usuarios:registro")

    def test_registro_usuario_no_autenticado(self):
        """
        Prueba que si un usuario no autenticado
        trata de usar la vista se le permite usarla
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    def test_registro_usuario_autenticado(self):
        """
        Prueba que si un usuario autenticado trata
        de entrar a la vista de registro va a hacer rechazado
        """
        login = reverse_lazy("usuarios:login")
        self.client.post(login, data={"username": "rafaelrs", "password": "jaja123"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_registrar_usuario_valido(self):
        """
        Prueba que un usuario con informacion
        valida puede registrarse
        """
        data = self.usuario_data
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_login_de_usuario_recien_registrado(self):
        """
        Prueba que un usuario con informacion valida recien
        registrado pueda loggearse
        """
        login = reverse_lazy("usuarios:login")
        data = self.usuario_data
        self.client.post(self.url, data=data, format='json')
        response = self.client.post(login, data={"username": "danielrs", "password": "jaja123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

class AdministracionCrearUsuariosViewTest(APITestCase):
    """
    Clase que contiene las pruebas de la
    vista que se encarga de la creacion de
    usuarios por parte del administrador
    """
    def setUp(self):
        """
        Llena la base de datos con informacion
        inicial para correr las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.superusuario = Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            email="danielrs9705@gmail.com",
            grupo=self.grupos[0],
            username="danielrs",
            is_superuser=True,
        )
        self.superusuario.set_password('jaja123')
        self.superusuario.save()
        self.admin = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafael@gmail.com",
            grupo=self.grupos[1],
            username="rafaelrs",
        )
        self.admin.set_password('jaja123')
        self.admin.save()
        self.vendedor = Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            email="david@gmail.com",
            grupo=self.grupos[2],
            username="dwest06",
        )
        self.vendedor.set_password('jaja123')
        self.vendedor.save()
        self.usuario_data = {
            "first_name": "Cruz",
            "last_name" : "Sanchez",
            "email"     : "crucita@hotmail.com",
            "username"  : "crucita",
            "password"  : "jaja123",
            "repeat_password" : "jaja123",
            "grupo"     : self.grupos[1].pk
        }
        self.url = reverse_lazy("usuarios:crear")
        self.login = reverse_lazy("usuarios:login")

    def test_de_la_vista(self): # pylint: disable=no-self-use
        """
        Prueba que la vista este creada
        """
        views.AdministracionCrearUsuariosView.as_view()

    # -------------- GRUPO DE PRUEBAS CON RESPECTO A LOS PERMISOS DE QUIENES PUEDEN VER LA VISTA--#
    def test_entrar_a_la_vista_no_autenticado(self):
        """
        Prueba que si un usuario no autenticado
        trata de entrar a la vista no se le permite
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_entrar_a_la_vista_autenticado_como_usuario_normal(self):
        """
        Prueba que si un usuario autenticado como
        usuario normal (Cliente, Vendedor) sera
        rechazado
        """
        self.client.post(self.login, data={"username": "dwest06", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_entrar_a_la_vista_como_admin(self):
        """
        Prueba que un usuario autenticado como
        administrador se le permite entrar a la
        vista
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    def test_entrar_a_la_vista_como_superusuario(self):
        """
        Prueba que un usuario autenticado como
        superusuario se le permite entrar a la
        vista
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED,
                         msg=response.data)

    #-------------------------------------------------------------------------------------------- #
    #-GRUPO DE PRUEBAS DE LOS USUARIOS QUE SE PUEDEN CREAR EN ESTA VISTA------------------------- #

    def test_superusuario_crea_administrador(self):
        """
        Prueba que un superusuario puede crear
        un administrador
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        response = self.client.post(self.url, data=self.usuario_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_superusuario_crea_usuario_normal(self):
        """
        Prueba que un superusuario puede crear
        un usuario normal (Cliente, Vendedor)
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        data = self.usuario_data
        data['grupo'] = self.grupos[2].pk
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_administrador_crea_administrador(self):
        """
        Prueba que un administrador puede crear
        otro administrador
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        data = self.usuario_data
        data['grupo'] = self.grupos[1].pk
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_administrador_crea_usuario_normal(self):
        """
        Prueba que un administrador puede crear un
        usuario normal
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        data = self.usuario_data
        data['grupo'] = self.grupos[2].pk
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)

    def test_administrador_crea_superusuario(self):
        """
        Prueba que un administrador no puede crear un
        superusuario
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        data = self.usuario_data
        data['grupo'] = self.grupos[0].pk
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, msg=response.data)

    # ------------------------------------------------------------------------------------------- #

class AdministracionUsuariosViewTest(APITestCase): # pylint: disable=too-many-instance-attributes
    """
    Clase que contiene las pruebas relacionadas a la
    vista de administracion de usuarios
    """
    def setUp(self):
        """
        Metodo que inicializa la base de datos
        con informacion para realizar las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.superusuario = Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            email="danielrs9705@gmail.com",
            grupo=self.grupos[0],
            username="danielrs",
            is_superuser=True,
        )
        self.superusuario.set_password('jaja123')
        self.superusuario.save()
        self.admin = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafael@gmail.com",
            grupo=self.grupos[1],
            username="rafaelrs",
        )
        self.admin.set_password('jaja123')
        self.admin.save()
        self.admin_2 = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafaelrs975@gmail.com",
            grupo=self.grupos[1],
            username="rafaeljunior",
        )
        self.admin_2.set_password('jaja123')
        self.admin_2.save()
        self.vendedor = Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            email="david@gmail.com",
            grupo=self.grupos[2],
            username="dwest06",
        )
        self.vendedor.set_password('jaja123')
        self.vendedor.save()
        self.cliente = Usuario.objects.create(
            first_name="Bertha",
            last_name="Palaos",
            email="bertha@gmail.com",
            grupo=self.grupos[3],
            username="bertha",
        )
        self.cliente.set_password('jaja123')
        self.cliente.save()
        self.usuario_data = {
            "first_name": "Cruz",
            "last_name" : "Sanchez",
            "email"     : "crucita@hotmail.com",
            "username"  : "crucita",
            "password"  : "jaja123",
            "repeat_password" : "jaja123",
            "grupo"     : self.grupos[1].pk
        }
        self.url_superusuario = reverse_lazy("usuarios:administracion",
                                             args=(self.superusuario.pk,))
        self.url_admin = reverse_lazy("usuarios:administracion", args=(self.admin.pk,))
        self.url_admin_2 = reverse_lazy("usuarios:administracion", args=(self.admin_2.pk,))
        self.url_vendedor = reverse_lazy("usuarios:administracion", args=(self.vendedor.pk,))
        self.url_cliente = reverse_lazy("usuarios:administracion", args=(self.cliente.pk,))
        self.login = reverse_lazy("usuarios:login")

    def test_de_la_vista(self): # pylint: disable=no-self-use
        """
        Prueba que la vista funciona
        """
        views.AdministracionUsuariosView.as_view()

    def test_url_de_la_vista(self):
        """
        Metodo que prueba el url que tiene
        conectado la vista
        """
        self.assertEqual("/usuarios/admin/detalle/1",
                         reverse_lazy("usuarios:administracion", args=(1,)))
        self.assertEqual("/usuarios/admin/detalle/2",
                         reverse_lazy("usuarios:administracion", args=(2,)))
        self.assertEqual("/usuarios/admin/detalle/3",
                         reverse_lazy("usuarios:administracion", args=(3,)))

    # ----------PRUEBAS QUE VERIFICA QUIENES PUEDEN ACCEDER A ESTA VISTA------------------------- #
    def test_usuario_no_autenticado_trata_acceder(self):
        """
        Metodo que prueba que un usuaario no autenticado
        no puede entrar a la vista
        """
        response = self.client.get(self.url_superusuario)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_superusuario_quiere_ver_detalles_administrador(self):
        """
        Metodo que prueba que si, un superusuario
        puede ver los datos de un administrador
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_usuario_superusuario_quiere_ver_detalles_usuario_normal(self):
        """
        Metodo que prueba que un superusuario puede
        ver los detalles de un usuario normal
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_vendedor)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_usuario_administrador_quiere_ver_detalles_superusuario(self):
        """
        Metodo que prueba que un usuario autenticado
        como administrador quiere ver los detalles de un
        superusuario no se lo permite
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_superusuario)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_administrador_quiere_ver_detalles_administrador(self):
        """
        Metodo que prueba que un administrador no
        puede ver los detalles de otro administrador
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_admin_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_administrador_quiere_ver_detalles_vendedor(self):
        """
        Metodo que prueba que un administrador si
        puede ver los detalles de un vendedor
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_vendedor)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_usuario_administrador_quiere_ver_detalles_cliente(self):
        """
        Metodo que prueba que un administrador si
        puede ver los detalles de un vendedor
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url_cliente)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
    # ------------------------------------------------------------------------------------------- #
    # ---GRUPO DE PRUEBAS SOBRE LA ELIMINACION EN ESTA VISTA------------------------------------- #
    def test_superusuario_puede_eliminar_administrador(self):
        """
        Metodo que prueba que un superusuario puede eliminar
        a un administrador
        """
        self.client.post(self.login, data={"username": "danielrs", "password": "jaja123"},
                         format='json')
        response = self.client.delete(self.url_admin)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_administrador_no_puede_eliminar_superusuario(self):
        """
        Metodo que prueba que un superusuario puede eliminar
        a un superusuario
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.delete(self.url_superusuario)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_administrador_no_puede_eliminar_administrador(self):
        """
        Metodo que prueba que un administrador no puede
        eliminar a otro administrador
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.delete(self.url_admin_2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_administrador_puede_eliminar_vendedor(self):
        """
        Metodo que prueba que un administrador puede eliminar
        a un vendedor
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.delete(self.url_vendedor)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    def test_administrador_puede_eliminar_cliente(self):
        """
        Metodo que prueba que un administrador puede eliminar
        a un cliente
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"},
                         format='json')
        response = self.client.delete(self.url_cliente)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, msg=response.data)

    # ------------------------------------------------------------------------------------------- #

class VendedorUsuarioView(APITestCase): # pylint: disable=too-many-instance-attributes
    """
    Clase que contiene las pruebas de la vista
    de Vendedor
    """
    def setUp(self):
        """
        Inicializa la base de datos con informacion
        para poder correr las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.superusuario = Usuario.objects.create(
            first_name="Daniel",
            last_name="Rodriguez",
            email="danielrs9705@gmail.com",
            grupo=self.grupos[0],
            username="danielrs",
            is_superuser=True,
        )
        self.superusuario.set_password('jaja123')
        self.superusuario.save()
        self.admin = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafael@gmail.com",
            grupo=self.grupos[1],
            username="rafaelrs",
        )
        self.admin.set_password('jaja123')
        self.admin.save()
        self.admin_2 = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafaelrs975@gmail.com",
            grupo=self.grupos[1],
            username="rafaeljunior",
        )
        self.admin_2.set_password('jaja123')
        self.admin_2.save()
        self.vendedor = Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            email="david@gmail.com",
            grupo=self.grupos[2],
            username="dwest06",
        )
        self.vendedor.set_password('jaja123')
        self.vendedor.save()
        self.cliente = Usuario.objects.create(
            first_name="Bertha",
            last_name="Palaos",
            email="bertha@gmail.com",
            grupo=self.grupos[3],
            username="bertha",
        )
        self.login = reverse_lazy("usuarios:login")
        self.url = reverse_lazy("usuarios:vendedor_detalles", args=(1,))
        self.usuarios = ["danielrs", "rafaelrs", "dwest06"]

    def test_de_la_vista(self): # pylint: disable=no-self-use
        """
        Metodo que prueba la existencia de la vista
        """
        views.VendedorUsuarioView.as_view()

    def test_url_de_la_vista(self):
        """
        Metodo que prueba la existencia de un url
        para la vista
        """
        self.assertEqual("/usuarios/vendedor/detalles/1",
                         reverse_lazy("usuarios:vendedor_detalles", args=(1,)))

    # ------GRUPO DE PRUEBAS DE LOS PERMISOS DE QUIENES PUEDEN VER ESTA VISTA-------------------- #
    def test_usuario_tiene_que_estar_autenticado(self):
        """
        Prueba que el usuario tiene que estar
        autenticado para ver la vista
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_solo_vendedor_puede_acceder_a_esta_vista(self):
        """
        Prueba que solo los vendedores
        pueden entrar en esta vista
        """
        for usuario in ["danielrs", "rafaelrs", "bertha"]:
            self.client.post(self.login, data={"username": usuario, "password": "jaja123"},
                             format='json')
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)
            self.client.logout()
        self.client.post(self.login, data={"username": "dwest06", "password": "jaja123"},
                         format='json')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND, msg=response.data)

    # -----GRUPO DE PRUEBAS QUE EL VENDEDOR SOLO ACCEDE A LOS DETALLES DE LOS CLIENTES ---------- #
    def test_vendedor_solo_puede_ver_los_detalles_de_un_cliente(self):
        """
        Prueba que un vendedor solo puede
        ver detalles de los clientes
        """
        self.client.post(self.login, data={"username": "dwest06", "password": "jaja123"},
                         format='json')
        id_usuarios = [
            Usuario.objects.get(username=username).pk for username in self.usuarios
        ]
        for ids in id_usuarios:
            url = reverse_lazy("usuarios:vendedor_detalles", args=(ids,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

        url_cliente = reverse_lazy("usuarios:vendedor_detalles", args=(self.cliente.pk,))
        response = self.client.get(url_cliente)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
    # ------------------------------------------------------------------------------------------- #

class PerfilViewTest(APITestCase):
    """
    Suite que contiene las pruebas
    con respecto a la vista que se encarga
    de modificar la informacion del usuario
    que esta loggeado
    """
    def setUp(self):
        """
        Inicializa la base de datos con informacion
        para correr las pruebas
        """
        self.grupos = [
            Group.objects.create(name=grupo) for grupo in GRUPOS
        ]
        self.admin = Usuario.objects.create(
            first_name="Rafael",
            last_name="Rodriguez",
            email="rafael@gmail.com",
            grupo=self.grupos[1],
            username="rafaelrs",
        )
        self.admin.set_password('jaja123')
        self.admin.save()
        self.vendedor = Usuario.objects.create(
            first_name="David",
            last_name="Rodriguez",
            email="david@gmail.com",
            grupo=self.grupos[2],
            username="dwest06",
        )
        self.vendedor.set_password('jaja123')
        self.vendedor.save()
        self.login = reverse_lazy("usuarios:login")

    def test_existencia_de_la_vista(self): # pylint: disable=no-self-use
        """
        Prueba que la vista exista
        """
        views.PerfilView.as_view()

    def test_existencia_de_un_url_para_la_vista(self):
        """
        Metodo que prueba que existe un url
        que conecta a la vista
        """
        self.assertEqual("/perfil/1",
                         reverse_lazy("usuarios:perfil", args=(1,)), msg="Los urls no son iguales")

    # ----GRUPO DE PRUEBAS DE QUIENES PUEDEN VER LA VISTA---------------------------------------- #
    def test_usuario_no_autenticado_entra_a_la_vista(self):
        """
        Metodo que prueba que un usuario no
        autenticado no puede entrar a la vista
        de perfil
        """
        url = reverse_lazy("usuarios:perfil", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_entra_a_perfil_de_otro_usuario(self):
        """
        Metodo que prueba que un usuario no puede
        entrar al perfil de otro usuario
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"})
        otro_usuario = Usuario.objects.get(username="dwest06")
        url_perfil = reverse_lazy("usuarios:perfil", args=(otro_usuario.pk,))
        response = self.client.get(url_perfil)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, msg=response.data)

    def test_usuario_entra_en_su_perfil(self):
        """
        Metodo que prueba que un usuario si puede
        entrar a la vista de su perfil
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"})
        usuario_loggeado = Usuario.objects.get(username="rafaelrs")
        url_perfil = reverse_lazy("usuarios:perfil", args=(usuario_loggeado.pk,))
        response = self.client.get(url_perfil)
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)

    def test_usuario_modifica_su_perfil(self):
        """
        Metodo que prueba que un usuario si
        puede modificar su perfil
        """
        self.client.post(self.login, data={"username": "rafaelrs", "password": "jaja123"})
        usuario_loggeado = Usuario.objects.get(username="rafaelrs")
        url_perfil = reverse_lazy("usuarios:perfil", args=(usuario_loggeado.pk,))
        data = {
            "first_name": "Rafael",
            "last_name": "Rodriguez",
            "email": "hola@gmail.com",
            "grupo": self.grupos[1].pk,
            "username": "rafaelrs",
            "password": "jaja123"
        }
        response = self.client.put(url_perfil, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        usuario_loggeado = Usuario.objects.get(username="rafaelrs")
        email_cambiado = usuario_loggeado.email
        self.assertEqual("hola@gmail.com", email_cambiado, msg="No se actualizo el email")
