# Peninsule


Voici le répo de la SAE du S3 développé par Anis, Jules, Thimothée et Elouan.

Ce **monorépo** est composé en 2 parties majeurs:

- Une partie API développé principalement par Thimothée et Elouan

- Une partie front-end développé principalement par Anis et Jules


_Le troisième dossier a été utilisé pour peupler la base de données pour les phases de développement. Les méthodes de génération de données ont été diverses: [IA](https://chat.openai.com/), [generatedata.com](https://generatedata.com/) ou bien à la main._


## Partie API


Pour le choix de la technologie utilisé nous avons fait le choix de FastAPI car facile de prise en main et très polyvalent. En effet, pour ce genre de petit projet, FastAPI est vraiment très adapté, il est facile à apprendre et tous les membres du projet ont pu comprendre son utilisation assez rapidement.


Combiné à cela, nous avons utilisé un **ORM** nommé **sqlalchemy**. Nous avons trouvé pertinent d'utiliser une telle technologie, car nous pensons qu'il est important de ce former à ce genre de chose car elle seront souvent utilisé en entreprise.

De plus, un orm permet de convertir le modèle de données à différents types de base de données ([Postgresql](https://www.postgresql.org/), [SQLite](https://www.sqlite.org/index.html), [MySql](https://www.mysql.com/fr/)...)

Actuellement, nous utilisons une base de données avec SQLite car il est vraiment **simple** de configurer un fichier .db. Nous pouvons ainsi nous partager le fichier assez simplement ce qui est vraiment pratique pour les phases de développement.

En revanche, nous pourrons installer un serveur **postgresql** pour le S4 pour pouvoir faire une base de données plus performante avec par exemple des triggers ou bien des backups. Ces actions ne sont pas impossibles à réaliser avec SQLite mais elles sont plus complexes.


Pour ce qui est de la partie de la gestion des utilisateurs nous avons un endpoint qui permet de générer un **token JWT** en vérifiant les informations saisit par l'utilisateur. Ainsi, le site web peut stocker le token et le passer dans le header des requêtes qui nécécitent d'être authentifiés. Par exemple pour requêter l'endpoint pour la récupération des informations d'utilisateur ce dernier doit fournir un **token valide** (durée de 30min) pour pouvoir avoir les infomations correspondante.


## Partie front-end

Pour le choix de la technologie utilisée, nous avons opté pour le framework JavaScript Svelte, qui permet de créer des applications web réactives. Notre choix a été motivé par la grande performance du framework, et par sa documentation bien fournie, comprenant même des exercices, pour une prise en main plus rapide.

Concrètement, notre dossier front-end contient divers fichiers et répertoires à contenus variés, la plupart ayant été générés à la création du projet. Les fichiers dont nous sommes les auteurs sont contenus dans le fichier "src". Au sein de ce dossier, se trouvent le répertoire "img", qui contient toutes les images que nous utilisons sur notre site, et le répertoire "routes", qui contient nos pages.

Dans le répertoire "routes" se trouvent de nombreux dossier. Le dossier "composants" contient la plupart des composants svelte appelés de parts et d'autres de notre site, et les autres fichiers correspondant aux pages du site. A l'exception de "compte", "connexion" et dashboardAdmin", ces dossiers ne contiennent qu'une page appelée +page.svelte qui contient l'ensemble du code de cette page.

Enfin, on retrouve les pages +page.svelte, qui est ouverte au lancement du projet, la page +layout.svelte qui permet l'affichage du header et du footer automatiquement sur toutes les pages, la page +erreur.svelte, qui est ouverte dans le cas d'une page introuvable (404) ou autres types d'erreur, et la page function.js (dont nous ne nous sommes pas beaucoup servi), qui contient des fonctions js accessibles depuis les autres pages.


### Partie Dev-ops


Nous avons mis à profit les fonctionnalités de GitLab, pour pouvoir faire des tests lors de la mise en ligne sur la branche main.

En effet, nous avons mis en place un workflow (que vous pouvez trouver à la racine du projet). Ce dernier permet de tester quelques enpoints -environ une quizaine- pour voir si ils fonctionnent bien. Les endpoints vérifiés étant les plus importants cela nous permet de vérifier qu'il n'y ai pas de bug dans notre code.

Nous avons commencé de faire un déploiement d'un docker sur dockerhub une fois les tests passés, mais nous avons rencontré quelques problèmes, nous poursuivrons donc le travail au quatrième semestre.

Le but final étant de déployer l'api ainsi que le site web sur un serveur avec kubernetes en utilisant des docker pour la conteneurisation. La pipeline nous permettrait de mettre directement les modifications en production dès lors que le code est envoyé sur la branche main du projet GitLab
