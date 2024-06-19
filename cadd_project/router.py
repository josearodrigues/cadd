
class DatabaseRouter(object):
    """
    Determina como rotear chamadas de banco de dados para os modelos
    """

    def db_for_read(self, model, **hints):

        # Todas as operações de leitura do app accounts são enviadas ao modelo default
        if model._meta.app_label == 'accounts':
            return 'default'
        # Todas as operações de leitura do app cadd são enviadas ao modelo default
        if model._meta.app_label == 'cadd':
            return 'default'
        # Todas as operações de leitura do app sca são enviadas ao modelo sca
        if model._meta.app_label == 'sca':
            return 'sca'
        return None

    def db_for_write(self, model, **hints):

        # Todas as operações de escrita do app accounts são enviadas ao modelo default
        if model._meta.app_label == 'accounts':
            return 'default'
        # Todas as operações de escrita do app cadd são enviadas ao modelo default
        if model._meta.app_label == 'cadd':
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Determina se relacionamentos são permitidos entre dois objetos"""

        # Permite qualquer relacionamento entre os dois modelos de banco de dados
        if obj1._meta.app_label == 'cadd' and obj2._meta.app_label == 'sca':
            return True

        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Determina que os modelos sejam criados no banco de dados correto"""

        if app_label == 'sca':
            return db == 'sca'
        elif db == 'cadd':
            return False

        return None
