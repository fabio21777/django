# Models

Campos

Existe algumas palavras resevadas que não podem ser usadas como nome de campo,como por exemplo:
- clean
- save
- delete

## tipos de campos de model
Todos os atributos devem ser instanciados a partir da classe `Field` apropriada, que é uma classe que representa um campo de banco de dados.

* Tipo da coluna (e.g. INTEGER, VARCHAR, TEXT).
* O widget padrão a ser usado na interface do administrador.
* A validação padrão a ser feita no campo.

## opções de modelos
Cada campo recebe um certo conjunto de argumentos específicos

-- link referência: https://docs.djangoproject.com/pt-br/5.0/ref/models/fields/#model-field-types
--

### null

Se True, o campo é permitido aceitar valores nulos.

### blank

Se True, o campo é permitido ser em branco. o padrão é false

### choices (enuns)


O primeiro elemento de cada tupla é o valor que será armazenado no banco de dados. O segundo elemento é exibido pelo widget de formulário do campo.

Dada uma instância de modelo, o valor de exibição de um campo choicespode ser acessado usando o get_FOO_display() método. Por exemplo

### default

O valor padrão para o campo. Pode ser um valor ou uma chamada de função sem argumentos.

### help_text

Texto de ajuda para o campo. Exibido com o widget do formulário.

### primary_key

Se True, este campo é a chave primária do modelo.Se você não especificar primary_key=True para qualquer campo, Django adicionará automaticamente um campo AutoField para armazenar a chave primária.

### unique

Se True, este campo deverá ser exclusivo em toda a tabela.
