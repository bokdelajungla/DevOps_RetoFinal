# Declaración y configuración de infraestructura

Para crear y configurar la infraestructura se ha elegido Vagrant y Ansible.

Vagrant nos crea un workflow para poder automatizar las tareas de crear maquinas virtuales.
```
# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"
Vagrant.require_version ">= 1.6.0"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
 config.vm.provision :ansible do |ansible|
    ansible.playbook = "playbook.yml"
  ENV['VAGRANT_DEFAULT_PROVIDER'] = 'docker'
  
  config.vm.provider "docker" do |d|
    d.build_dir = "."
    d.has_ssh = true
d.remains_running = true
  end
 
end

```
Se le añade el playbook con Ansible para poder configurar los enternos.
```
- hosts: localhost
  become: true
  tasks:
  - debug:
      var: ansible_os_family

  
  - name: "Install docker"
    package: 
      name: "docker-ce-18.09.1-3.el7.x86_64"
      state: present

  - name: "Install pip"
    package: 
      name: "python3-pip"
      state: present
      update_cache: true
    
  - name: "Install docker sdk"
    pip:
     name: "docker"
 
  # - name: "Update docker service"
  #   replace:
  #      path: "/lib/systemd/system/docker.service"
  #      regexp: "^ExecStart.*"
  #      replace: "ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:4243"
  #   notify: 
  #   - "Restart docker"
  #   - "Reload deamon"
  
  - name: "Start docker service"
    service:
      name: "docker"
      state: started
```



