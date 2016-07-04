#Vornei: 01/07/2016 - Programa para fazer o backup das imagens
# das VMs que estao em /var/lib/libvirt/images, serah feito apenas o backup
# dos arquivos de extensao .img.
# Este programa em python tem caracteristica/comportamento paraceido com script shell
# se for executado sem parametro (Ex.: python host01_images_vm_bkp.py), farah o bkp
#  de todas VMs automatico, porem se for passado o nome da imagem especifica 
# (Ex. python host01_images_vm_bkp.py vm.img), farah o backup paenas da imagem desejada
import os, glob, sys
from datetime import datetime
#from shutil import make_archive

dirImg = '/var/lib/libvirt/images/'
dirBkp = '/bkp/host01/images_vm/'
dt = datetime.now()
#Lista das VMs que precisam ser paradas antes de copiar
#Ex. listaVmsParar = ["zabbix.img", "dac08.img",]
listaVmsParar = []

def vm_stop(vm):
    print "### Verificar se a VM "+ vm +" precisa ser parada..."
    if vm in listaVmsParar:
	vmNome = vm.split(".")[0]
	print("#### Parando VM "+ vmNome +" ...")
        if (os.system("virsh shutdown "+ vmNome)):
            print("ERRO! Possibilidades: A VM pode estar parada ou o usuario nao tem permissao para shutdown. ")
        else:
            print("OK!")
    else:
        print("#### Nao precisa!")

def vm_start(vm):
    print "### Verificar se a VM "+ vm +" precisa ser iniciada..."
    if vm in listaVmsParar:
        vmNome = vm.split(".")[0]
        print("#### Iniciando VM "+ vmNome +" ...")
        if (os.system("virsh start "+ vmNome)):
            print("ERRO! Possibilidades: A VM nao esta parada ou o usuario nao tem permissao para start.")
        else:
            print("OK!")

def vm_bkp(img):
    vm_stop(img)
    #Verificar se o diretorio de BKP existe, caso nao exista, criarah
    dirVMBkp = dirBkp + img.split(".")[0] +"/"
    if not os.path.exists(dirVMBkp):
        print "Criando diretorio "+ dirVMBkp
        #os.system("mkdir -p "+ dirVMBkp)
        os.makedirs(dirVMBkp)
    nomeArqGz = dirVMBkp + img +".tar.gz"
    nomeArqGzOld = dirVMBkp +"old_"+ img +".tar.gz"

    if os.path.isfile(nomeArqGz):
        
        if os.path.isfile(nomeArqGzOld):
            print "Apagando "+ nomeArqGzOld +" ..."
    	    os.unlink(nomeArqGzOld)

        print "Renomeando: "+ nomeArqGz +" para "+ nomeArqGzOld
        os.rename(nomeArqGz, nomeArqGzOld)

    os.system("tar -zcv "+ dirImg + img +" > "+ nomeArqGz)
    #make_archive(dirImg + img, "gztar", nomeArqGz)
    vm_start(img)

print "Backup das Imagens das VMs - ("+ str(dt) +")"
print "Listando arquivos (Dir: "+ dirImg +"):"
print os.listdir(os.path.expanduser(dirImg)) #listando todos os arquivos no diretorio
print "Backup apenas dos arquivos .img"
os.chdir(dirImg) #abrindo o diretorio

print "Verificando tipo do Backup [PARAMETRO]..."
if len(sys.argv) == 1:
    #Se for caso de Backup Automatico em Lote, nenhum parametro foi passado
    print "# Iniciando o Backup Automatico dos Arquivos .img"

    for img in glob.glob("*.img"):
        print("## VM: "+ img +":")
        vm_bkp(img)

else:
    #Senao eh caso de Backup especifico o nome do arquivo foi digitado
    #O parametro do backup expecifico eh o nome do arquivos
    nomeArq = sys.argv[1]
    print "# Iniciando o Backup para Arquivo especifico: "+ nomeArq
    
    if os.path.isfile(nomeArq):
        vm_bkp(img)
        
    else:
        print "Arquivo Inexistente!"
