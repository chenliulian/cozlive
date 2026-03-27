variable "aws_region" {
  description = "AWS 区域"
  type        = string
  default     = "ap-southeast-1"
}

variable "environment" {
  description = "环境名称 (development, staging, production)"
  type        = string
  default     = "development"
}

variable "vpc_cidr" {
  description = "VPC CIDR 块"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "可用区列表"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"]
}

variable "private_subnet_cidrs" {
  description = "私有子网 CIDR 列表"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "公有子网 CIDR 列表"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# EKS 节点配置
variable "node_desired_size" {
  description = "节点期望数量"
  type        = number
  default     = 2
}

variable "node_min_size" {
  description = "节点最小数量"
  type        = number
  default     = 1
}

variable "node_max_size" {
  description = "节点最大数量"
  type        = number
  default     = 5
}

variable "node_instance_types" {
  description = "节点实例类型"
  type        = list(string)
  default     = ["t3.medium", "t3.large"]
}

variable "ai_node_desired_size" {
  description = "AI 节点期望数量"
  type        = number
  default     = 1
}

variable "ai_node_min_size" {
  description = "AI 节点最小数量"
  type        = number
  default     = 0
}

variable "ai_node_max_size" {
  description = "AI 节点最大数量"
  type        = number
  default     = 3
}

# RDS 配置
variable "db_instance_class" {
  description = "RDS 实例类型"
  type        = string
  default     = "db.t3.medium"
}

variable "db_allocated_storage" {
  description = "RDS 初始存储大小 (GB)"
  type        = number
  default     = 100
}

variable "db_max_allocated_storage" {
  description = "RDS 最大存储大小 (GB)"
  type        = number
  default     = 1000
}

# Redis 配置
variable "redis_node_type" {
  description = "Redis 节点类型"
  type        = string
  default     = "cache.t3.micro"
}
