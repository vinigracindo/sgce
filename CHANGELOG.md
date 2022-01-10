# Changelog
Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
e o projeto adere ao [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.4.1] - 2022-01-10
### Added
- Fix (#17).
- Atualizado requirements

## [1.4.0] - 2021-02-05
### Added
- Fix (#16).
- Adicionado deploy com Docker.
- Removido dependência com o python-decouple.
- Adicionado o atributo has_public_page no Evento. Na migração (0005_auto_20201116_0945) coloca False como default em todos os eventos já criados. Caso seja True, o evento poderá cer acessado através da url /event/<slug_field> e todos os certificados do evento serão mostrados na página.

## [1.3.0] - 2020-08-28
### Added
- Adicionado Edição do Perfil Logado (#11).
- Adicionado o atributo has_qrcode no Modelo do Certificado. Na migração (0005_auto_20200828_1230) coloca True como default em todos os certificados já criados. Caso seja False, o certificado não vem com QRCode.
- Adicionado o atributo is_public no Modelo do Certificado. Na migração (0006_template_is_public) coloca como False em todos os certificados. Antes todos os modelos eram públicos para todos os usuários cadastrados no sistema. Agora só fica público se este campo bolleano for marcado.
- Adicionado na criação/edição de um certificado a página de configuração onde é possível setar o is_public e o has_qrcode.
- Fix #12 - Aumentado o max_length dos atributos do Modelo e dos Eventos (0007_auto_20200828_1812).
- Atualizado as dependências do projeto.

## [1.2.1] - 2020-06-08
###Changed
- Atualizado as dependências inseguras do projeto.

## [1.2.0] - 2019-07-12
### Added
- Melhorado a tela administrativa para Eventos, Participantes e Modelos.
### Changed
- Atualizado as dependências inseguras do projeto.

## [1.1.0] - 2019-06-07
### Added
- Fix #1
- Fix #2
- Merge pull request #4

## [1.0.1] - 2019-03-07
### Changed
- Altera composição do título do certificado gerado por questões de incompatibilidade com gunicorn

## [1.0.0] - 2019-02-27
### Added
- Gerenciamento de Usuários
- Gerenciamento de Eventos
- Gereciamento de Particpantes
- Gerenciamento de Modelos de Certificados

[Em desenvolvimento]: https://github.com/vinigracindo/sgce/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/vinigracindo/sgce/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/vinigracindo/sgce/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/vinigracindo/sgce/compare/v1.0.0...v1.0.1
