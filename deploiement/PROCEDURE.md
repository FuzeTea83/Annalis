# Procédure de déploiement des VM

## Résaux
1. **VM 1 (Proxy) :** Configuration avec 2 adaptateurs réseau. Adaptateur 1 en NAT (avec redirection de port 8080 vers 80). Adaptateur 2 en "Réseau interne" nommé `intnet-app`.
2. **VM 2 (Métier) :** Configuration avec 1 seul adaptateur en "Réseau interne" (`intnet-app`).
3. **VM 3 (Données) :** Configuration avec 1 seul adaptateur en "Réseau interne" (`intnet-app`).

## Netplan
Sur chaque machine, modification des fichiers YAML dans `/etc/netplan/` pour attribuer les adresses IP fixes, suivi de la commande `sudo netplan apply` :
* **VM 1 (Proxy) :** 10.10.10.10/24 sur l'interface réseau interne.
* **VM 2 (Métier) :** 10.10.10.20/24.
* **VM 3 (Données) :** 10.10.10.30/24.

## MariaDB
1. Modification du fichier de configuration MariaDB (`/etc/mysql/mariadb.conf.d/50-server.cnf`).
2. Remplacement de la ligne `bind-address` par `bind-address = 10.10.10.30` pour autoriser les connexions provenant du réseau interne.
3. Redémarrage du service : `sudo systemctl restart mariadb`.

## FastAPI
1. Transfert du code source (dossier `app`, `alembic` et fichiers racines) vers `/home/user/VM/` via SCP (en rebondissant par la VM 1 si besoin).
2. Configuration du fichier `.env` pour pointer vers la base de données : `DATABASE_URL=mysql+pymysql://user:password@10.10.10.30:3306/annalis`.
3. Application des migrations de base de données à la racine du projet :
   ```bash
   source venv/bin/activate
   alembic upgrade head
   ```
   
## Exécution en arrière-plan du serveur
1. Création de l'unité systemd (`/etc/systemd/system/api.service`)
2. Activer les services pour démarrer automatiquement au boot :
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now api.service
   ```
   
## Déploiement du Frontend
1. `sudo rm -rf /var/www/html/*`
2. Compiler le Vue.js (`npm run build`) et copier le contenu du dossier `dist` vers `/var/www/html/` sur la VM front end.
3. Attribuer les permissions
```bash
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/
```
4. Modifier le proxy (`/etc/nginx/sites-available/default`)
5. Redémarrer Nginx : `sudo systemctl restart nginx`.