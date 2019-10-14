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
```
