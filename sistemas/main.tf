variable "vpc_cidr_block"{}
variable "public_subnet_cidr_block"{}
variable "public_subnet_cidr_block_ha"{}
variable "private_subnet_cidr_block"{}
variable "private_subnet_cidr_block_ha"{}
variable "all_ips"{}
variable "ssh_rsa"{}

provider "aws" {
  region = "eu-west-1"
}

resource "aws_vpc" "quantum_vpc" {
  //cidr_block = "10.3.0.0/16"
  cidr_block = "${var.vpc_cidr_block}"
  tags {
    Name = "quantum_vpc"
  }
}

//SUBNET PUBLICA
resource "aws_internet_gateway" "igw_quantum"{
  vpc_id = "${aws_vpc.quantum_vpc.id}"
  tags {
    Name = "igw_quantum"
  }
}

resource "aws_subnet" "quantum_public_subnet" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"
  cidr_block = "${var.public_subnet_cidr_block}"
  availability_zone = "eu-west-1a"
  tags {
    Name = "quantum_public_subnet"
  }
}

resource "aws_route_table" "quantum_public_route_table" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  route {
    cidr_block = "${var.all_ips}"
    gateway_id = "${aws_internet_gateway.igw_quantum.id}"
  }

  tags {
    Name = "quantum_public_route_table"
  }
}

resource "aws_route_table_association" "quantum_public_association" {
  subnet_id      = "${aws_subnet.quantum_public_subnet.id}"
  route_table_id = "${aws_route_table.quantum_public_route_table.id}"
  //vpc_id = "${aws_vpc.vpc_angel.id}"
}

//SUBNET PRIVADA
resource "aws_nat_gateway" "quantum_nat"{
  //vpc_id = "${aws_vpc.vpc_angel.id}"
  tags {
    Name = "quantum_nat"
  }
  allocation_id = "${aws_eip.aws_elastic_ip_nat.id}" //eip
  subnet_id = "${aws_subnet.quantum_public_subnet.id}"
}

resource "aws_subnet" "quantum_private_subnet" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"
  cidr_block = "${var.private_subnet_cidr_block}"
  availability_zone = "eu-west-1a"
  tags {
    Name = "quantum_private_subnet"
  }
}

resource "aws_route_table" "quantum_private_route_table" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  route {
    cidr_block = "${var.all_ips}"
    nat_gateway_id = "${aws_nat_gateway.quantum_nat.id}"
  }

  tags {
    Name = "quantum_private_route_table"
  }
}

resource "aws_route_table_association" "quantum_private_association" {
  subnet_id      = "${aws_subnet.quantum_private_subnet.id}"
  route_table_id = "${aws_route_table.quantum_private_route_table.id}"
}

resource "aws_eip" "aws_elastic_ip_nat" {
  vpc = true
  tags{
    Name = "quantum_eip"
  }
}

//Security group ELB
resource "aws_security_group" "quantum_sg_elb" {
  name        = "sg_webapp_quantum_elb"
  description = "security group quantum elb"
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["213.9.144.3/32"]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["${var.all_ips}"]
  }

  tags {
    Name = "sg_webapp_angel_elb"
  }
}

//Security group para el bastion
resource "aws_security_group" "sg_quantum_ec2_bastion" {
  name        = "sg_webapp_quantum_ec2_bastion"
  description = "security group quantum bastion"
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["${var.all_ips}"]
  }

  tags {
    Name = "sg_webapp_quantum_bastion"
  }
}

resource "aws_security_group_rule" "quantum_ingress_bastion_ssh"{
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  cidr_blocks = ["213.9.144.3/32"]
  security_group_id = "${aws_security_group.sg_quantum_ec2_bastion.id}"
  description = "bastion quantum allow ssh"
}


//Security group de la webapp
resource "aws_security_group" "sg_quantum_ec2_webapp" {
  name        = "sg_webapp_quantum_ec2_webapp"
  description = "security group quantum webapp"
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    cidr_blocks     = ["${var.all_ips}"]
  }

  tags {
    Name = "sg_webapp_quantum_webapp"
  }
}

resource "aws_security_group_rule" "quantum_ingress_webapp_http"{
  type = "ingress"
  from_port = 80
  to_port = 80
  protocol = "tcp"
  source_security_group_id = "${aws_security_group.quantum_sg_elb.id}"
  security_group_id = "${aws_security_group.sg_quantum_ec2_webapp.id}"
  description = "ec2 app quantum allow http"
}

resource "aws_security_group_rule" "quantum_ingress_webapp_ssh"{
  type = "ingress"
  from_port = 22
  to_port = 22
  protocol = "tcp"
  source_security_group_id = "${aws_security_group.sg_quantum_ec2_bastion.id}"
  security_group_id = "${aws_security_group.sg_quantum_ec2_webapp.id}"
  description = "ec2 app quantum allow ssh from bastion"
}


//--BALANCER--
resource "aws_elb" "elb_quantum"{
  name = "elb-quantum"
  security_groups = ["${aws_security_group.quantum_sg_elb.id}"]
  subnets = ["${aws_subnet.quantum_public_subnet.id}","${aws_subnet.quantum_public_subnet_ha.id}"]

  listener {
    instance_port     = 80
    instance_protocol = "http"
    lb_port           = 80
    lb_protocol       = "http"
  }
  instances = ["${aws_instance.ec2_quantum_app.id}","${aws_instance.ec2_quantum_app_ha.id}"]
  tags{
    Name = "elb_quantum"
  }

}

//Key pairs
resource "aws_key_pair" "quantum_key_pair" {
  key_name   = "quantum_key_pair"
  public_key = "${var.ssh_rsa}"

}



//Webapp
resource "aws_instance" "ec2_quantum_app"{
  ami = "ami-ca0135b3"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.quantum_private_subnet.id}"
  vpc_security_group_ids = ["${aws_security_group.sg_quantum_ec2_webapp.id}"]

  key_name = "${aws_key_pair.quantum_key_pair.key_name}"
  //user_data = "#!/bin/bash; yum install -y nginx; service nginx start"
  tags {
    Name = "ec2_quantum_app"
  }

  /*provisioner "file" {
    source      = "~/Quantum"
    destination = "/tmp"
  }
  connection {
    type = "ssh"
    user = "ec2-user"
    bastion_host = "${aws_instance.ec2_quantum_bastion.public_ip}"
    private_key = ""
    bastion_private_key = ""
    bastion_user = "ec2-user"
  }*/


}

//Bastion
resource "aws_instance" "ec2_quantum_bastion"{
  ami = "ami-ca0135b3"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.quantum_public_subnet.id}"
  associate_public_ip_address = true
  vpc_security_group_ids = ["${aws_security_group.sg_quantum_ec2_bastion.id}"]

  key_name = "${aws_key_pair.quantum_key_pair.key_name}"
  tags {
    Name = "ec2_quantum_bastion"
  }
}


// -- HA --

//PUBLIC SUBNET HA
resource "aws_subnet" "quantum_public_subnet_ha" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"
  cidr_block = "${var.public_subnet_cidr_block_ha}"
  availability_zone = "eu-west-1b"
  tags {
    Name = "quantum_public_subnet_ha"
  }
}

resource "aws_route_table" "quantum_public_route_table_ha" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  route {
    cidr_block = "${var.all_ips}"
    gateway_id = "${aws_internet_gateway.igw_quantum.id}"
  }

  tags {
    Name = "quantum_public_route_table_ha"
  }
}

resource "aws_route_table_association" "quantum_public_association_ha" {
  subnet_id      = "${aws_subnet.quantum_public_subnet_ha.id}"
  route_table_id = "${aws_route_table.quantum_public_route_table_ha.id}"
  //vpc_id = "${aws_vpc.vpc_angel.id}"
}


//PRIVATE SUBNET HA
resource "aws_subnet" "quantum_private_subnet_ha" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"
  cidr_block =  "${var.private_subnet_cidr_block_ha}"
  availability_zone = "eu-west-1b"
  tags {
    Name = "quantum_private_subnet_ha"
  }
}

resource "aws_route_table" "quantum_private_route_table_ha" {
  vpc_id = "${aws_vpc.quantum_vpc.id}"

  route {
    cidr_block = "${var.all_ips}"
    nat_gateway_id = "${aws_nat_gateway.quantum_nat.id}"
  }

  tags {
    Name = "quantum_private_route_table_ha"
  }
}

resource "aws_route_table_association" "quantum_private_association_ha" {
  subnet_id      = "${aws_subnet.quantum_private_subnet_ha.id}"
  route_table_id = "${aws_route_table.quantum_private_route_table_ha.id}"
}

// Webapp en HA
resource "aws_instance" "ec2_quantum_app_ha"{
  ami = "ami-ca0135b3"
  instance_type = "t2.micro"
  subnet_id = "${aws_subnet.quantum_private_subnet_ha.id}"
  vpc_security_group_ids = ["${aws_security_group.sg_quantum_ec2_webapp.id}"]

  key_name = "${aws_key_pair.quantum_key_pair.key_name}"
  //user_data = "#!/bin/bash; yum install -y nginx; service nginx start"
  tags {
    Name = "ec2_quantum_app_ha"
  }
}



