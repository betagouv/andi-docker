## Outil CRUD de gestion de base de données

Utilise une image docker, quelques fichiers de configuration et une version adaptée d'évolutility (l'outil crud en question)

Le docker contient l'API Graphql (server) et l'interface React (ui)

(still using default-assigned network, create docker subnet to fix this)
```
sudo docker build -t "evolutility" \
    --build-arg PG_USER=[USER] \
    --build-arg PG_PASS=[PASSWORD] \
    ./ && \
    sudo docker run -it --rm \
        --add-host=database:172.17.0.1 \
        -p=8080:3000 evolutility
```

### Liste de valeurs
Certains champs contiennent des listes de valeurs.
Afin de faciliter leur emploi, il convient de créer des vues sur base des données présentes dans la DB

Exemple:
```SQL
-- Taille entreprises
CREATE VIEW lov_taille AS SELECT taille AS ID, taille AS Name FROM entreprises GROUP BY TAILLE;
```
Dans d'autres cas des tableaux simples peuvent suffire:

```SQL
--
CREATE TABLE lov_ouinon ( ID VARCHAR(3), Name VARCHAR(3) );
INSERT INTO lov_ouinon VALUES ('oui', 'Oui'), ('non', 'Non');

CREATE TABLE lov_couverture ( ID TEXT, Name TEXT );
INSERT INTO lov_couverture VALUES
    ('un', 'Un'),
    ('tous', 'Tous'),
    ('tous_departement', 'Département'),
    ('tous_region', 'Région'),
    ('specifique_dep', 'Départements'),
    ('specifique_regions', 'Régions'),
    ('autre', 'Autre')
;


CREATE TABLE lov_acces ( ID TEXT, Name TEXT );
INSERT INTO lov_acces VALUES
    ('train', 'Train'),
    ('rer', 'RER'),
    ('metro', 'Metro'),
    ('bus', 'Bus'), 
    ('tram', 'Tram'),
    ('parking_pmr', 'Parking accessible PMR'),
    ('autre', 'Autre')
;

CREATE TABLE lov_pmr ( ID TEXT, Name TEXT );
INSERT INTO lov_pmr VALUES
    ('plain_pied', 'Accès de plain pied'),
    ('portes_automatiques', 'Portes automatiques'),
    ('portes_larges', 'Portes larges'),
    ('ascenseurs', 'Ascenseurs'),
    ('sanitaires_pmr', 'Sanitaires PMR'),
    ('rampes_access', 'Rampes d`accès'),
    ('restaurant_pmr', 'Restaurant PMR'),
    ('elevateur', 'Élévateur'),
    ('autre', 'Autre')
;

CREATE TABLE lov_amenagement ( ID TEXT, Name TEXT );
INSERT INTO lov_amenagement VALUES
    ('boucle_magneto', 'Boucles magnétiques'),
    ('bandes_pododactiles', 'Bandes pterodactiles'),
    ('ascenseurs_vocalises', 'Acenseurs vocalisés'),
    ('autre', 'Autre')
;

CREATE TABLE lov_materiel ( ID TEXT, Name TEXT );
INSERT INTO lov_materiel VALUES
    ('bureaux_postes_pmr', 'Bureaux et postes adaptés PMR'),
    ('fauteuils_ergo', 'Fauteuil(s) ergonomique(s)'),
    ('aides_visuel', 'Outils bureautiques et/ou techniques déficience visuelle'),
    ('aides_auditif', 'Outils bureautiques et/ou techniques déficience auditive'),
    ('aides_dyslexie', 'Outils bureautiques et/ou techniques personnes dyslexiques'),
    ('autre', 'Autre')
;

```
