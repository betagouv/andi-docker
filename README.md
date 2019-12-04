<p align="center">
  <a href="https://andi.beta.gouv.fr">
    <img alt="Début description. Marianne. Fin description." src="https://upload.wikimedia.org/wikipedia/fr/3/38/Logo_de_la_R%C3%A9publique_fran%C3%A7aise_%281999%29.svg" width="90" />
  </a>
</p>
<h1 align="center">
  andi.beta.gouv.fr
</h1>

[ANDi](https://andi.beta.gouv.fr) est une service numérique en développement visant à faciliter l'immersion professionnelle des personnes en situation de handicap.

# 🐳 andi-docker
Divers services sous docker utilisés par ANDi. Chaque répertoire est un service Docker contenant son propre `Dockerfile`. Le déploiement est assuré par le CI de Travis sur les serveurs d'ANDi, et détaillée dans le fichier `.travis.yml`.

Les services dockers sont des composants péripheriques du service d'ANDi, non critiques au service metier, mais néanmoins nécessaires à la réalisation de ses objectifs.

## evolutility
Backend (_CRUD Interface_) pour la base de données PostgreSQL utilisée par ANDi. Elle emploie les composans open-source suivants:
- https://github.com/evoluteur/evolutility-server-node
- https://github.com/evoluteur/evolutility-ui-react

Le répertoire contient les fichiers de base nécessaires à la configuration du serveur et de l'interface ANDi afin de pouvoir afficher et modifier les données des bases de données d'ANDi.

## form_handler
Composant particulier qui traite l'envoi des divers formulaires (_Landing page_, Journeaux de bord, ...). Le composant à les particularités suivantes, qui ont justifié sont développement:
- validation des champs et des données
- contrôle envois multiples
- notification **slack**
- notification **email**
- enregistrement BD
- enregistrement dans un CSV Local
- configuration via fichier yaml pour chaque type de formulaire gére

## public_graphql
Service **graphql** qui publie les éléments textuels utilisé par les composants d'ANDi (landing page, e-mails, ...). Celui-ci est en réalité le même composant _evolutility-server-node_ qu'utilisé pour le backoffice, configuré pour n'offrir qu'un accès restreint aux données d'ANDi.

## public_preview
Preview dynamique de la landing page, en développement

## sendbot
Bot d'envoi de courriels, intégré à airtable ou intégrable à tout autre outil ou sont définis les paramêtres nécessaires aux envois automatiques. Il est utilisé pour les rappels de remplissage du journal de bord.

