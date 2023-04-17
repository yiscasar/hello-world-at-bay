terraform {
  backend "s3" {
    key            = "terraform.tfstate"
    bucket         = "helloworld-tfstate"
    region         = "eu-west-1"
    dynamodb_table = "helloworld-tfstate"
  }
}
