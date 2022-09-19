docker volume create gitlab-runner-config-for-publish
docker run -d --name gitlab-runner-for-publish --restart always -v /var/run/docker.sock:/var/run/docker.sock -v gitlab-runner-config-for-publish:/etc/gitlab-runner gitlab/gitlab-runner:latest
docker run --rm -it -v gitlab-runner-config-for-publish:/etc/gitlab-runner gitlab/gitlab-runner:latest register --executor docker --docker-image "docker:20.10.16" --docker-privileged
