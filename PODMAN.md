# En el servidor, copiar la plantilla del repo
mkdir -p /opt/ph-app

sudo curl -s https://raw.githubusercontent.com/AL3X09/[repo]/master/.env.example \
  -o /opt/ph-app/front/.env

#permisos
sudo chown $USER:$USER /opt/ph-app/front/.env
# Luego editar con los valores reales
nano /opt/ph-app/.env
# o
vi /opt/ph-app/.env

# Proteger el archivo en muchos casos ni podman puede acceder
chmod 600 /opt/ph-app/.env
# build imagen
podman build   --no-cache   -t propiedad-horizontal:latest   https://github.com/AL3X09/[repo].git#master
podman build   --no-cache   -t propiedad-horizontal:latest   https://github.com/AL3X09/servicio_notificaciones.git#master

# crear el pod
podman pod create \
  --name servicio-notificaciones-pod \
  -p 8003:8002 \
  --network app-network

podman run -d   --name front-admin-app   --network app-network   --volume /opt/ph-app/front/.env:/app/.env:ro,Z   --restart unless-stopped   -p 8000:80   front-admin-app:latest

podman run -d   --name servicio_notificaciones-app   --network app-network   --volume /opt/ph-app/notification/.env:/app/.env:ro,Z   --restart unless-stopped   -p 8003:8002   servicio_notificaciones:latest

#
podman run -d   --name servicio_notificaciones-app  --pod servicio-notificaciones-pod   --volume /opt/ph-app/notification/.env:/app/.env:ro,Z   --restart unless-stopped   servicio-notificaciones:latest

podman run -d \
  --name servicio_notificaciones-app \
  --pod servicio-notificaciones-pod \
  --volume /opt/ph-app/notification/.env:/app/.env:ro,Z \
  --restart unless-stopped \
  servicio-notificaciones:latest


podman stop vue-admin 2>/dev/null; podman rm vue-admin 2>/dev/null
podman rm -f propiedad_horizontal-app

podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Networks}}"

podman logs -f propiedad_horizontal-app



File "/app/src/servicio_notificaciones/app/core/config.py", line 34, in <module>
    settings = Settings()