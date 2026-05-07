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

podman stop vue-admin 2>/dev/null; podman rm vue-admin 2>/dev/null
podman rm -f propiedad_horizontal-app

podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Networks}}"

podman logs -f propiedad_horizontal-app


podman run -d   --name front-admin-app   --network app-network   --volume /opt/ph-app/front/.env:/app/.env:ro,Z   --restart unless-stopped   -p 8000:80   front-admin-app:latest


/usr/local/lib/python3.14/site-packages/fastapi/openapi/utils.py:251: UserWarning: Duplicate Operation ID get_interiortorre_id_endpoint_casa_interior_links__interiortorre__id_get for function get_interiortorre_id_endpoint at /app/src/propiedad_horizontal/app/api/casa_interior_links.py
  warnings.warn(message, stacklevel=1)

