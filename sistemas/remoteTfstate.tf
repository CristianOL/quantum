terraform {
  backend "s3"{
    bucket = "angelsegovia-bucket"
    key = "terraform.tfstate"
    region = "eu-west-1"
  }
}