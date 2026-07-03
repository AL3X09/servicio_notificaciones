# En el servidor, copiar la plantilla del repo
mkdir -p /opt/ph-app

sudo curl -s https://raw.githubusercontent.com/AL3X09/[repo]/main/.env.example \
  -o /opt/ph-app/front/.env

sudo curl https://raw.githubusercontent.com/AL3X09/vue-admin/main/.env.example -o /opt/ph-app/notification/.env


#permisos
sudo chown $USER:$USER /opt/ph-app/front/.env
# Luego editar con los valores reales
nano /opt/ph-app/.env
# o
vi /opt/ph-app/.env

# Proteger el archivo en muchos casos ni podman puede acceder
chmod 600 /opt/ph-app/.env
#
podman volume create postgres_data_vol
#
podman network create app-network
# build imagen
podman build   --no-cache   -t [repo]:latest  https://github.com/AL3X09/[repo].git#master

podman build --no-cache   -t propiedad-horizontal:latest  https://github.com/AL3X09/propiedad_horizontal.git#master
podman build --no-cache   -t servicio-notificaciones:latest  https://github.com/AL3X09/servicio_notificaciones.git#master

#  vue
args=()
while IFS= read -r line; do
  args+=(--build-arg "$line")
done < <(grep ^VITE_ /opt/ph-app/front/.env)
podman build "${args[@]}"  --no-cache   -t vue-admin:latest  https://github.com/AL3X09/vue-admin.git#master




# Desde el contenedor propiedad_horizontal, verificar que resuelve el otro servicio
podman exec propiedad_horizontal-app curl http://servicio-notificaciones:8002/health


podman stop vue-admin 2>/dev/null; podman rm vue-admin 2>/dev/null
podman pod rm -f servicio-notificaciones-pod
podman rm -f propiedad_horizontal-app

podman ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Networks}}"

podman logs -f propiedad_horizontal-app

# ver imagenes
podman images ls

# borrar volumenes
Si no tienes datos importantes aún: 

podman volume rm postgres_data_vol

y luego podman volume create postgres_data_vol.