#!/bin/bash

# 生成私钥
openssl ecparam -name prime256v1 -genkey -out private_key.pem

# 生成证书请求
openssl req -new -sha256 -key private_key.pem -out certificate_request.pem -subj "/C=CN/ST=Beijing/L=Beijing/O=MyOrganization/OU=MyOrganizationalUnit/CN=localhost"

# 自签名证书
openssl x509 -req -days 365 -in certificate_request.pem -signkey private_key.pem -out self_signed_certificate.pem

# 验证证书
openssl x509 -text -noout -in self_signed_certificate.pem
