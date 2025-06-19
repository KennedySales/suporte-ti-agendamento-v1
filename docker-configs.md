
# Configurações Docker e DevOps

## 🐳 Docker

### Dockerfile (Backend)
```dockerfile
FROM node:18-alpine

# Instalar dumb-init para handle de sinais
RUN apk add --no-cache dumb-init

# Criar usuário não-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S helpdesk -u 1001

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY --chown=helpdesk:nodejs package*.json ./

# Instalar dependências
RUN npm ci --only=production && npm cache clean --force

# Copiar código fonte
COPY --chown=helpdesk:nodejs . .

# Mudar para usuário não-root
USER helpdesk

# Expor porta
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Comando de inicialização
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "src/server.js"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Backend API
  backend:
    build: 
      context: ./backend
      dockerfile: Dockerfile
    container_name: helpdesk-backend
    ports:
      - "3000:3000"
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      - NODE_ENV=production
      - DB_HOST=mysql
      - DB_USER=helpdesk_user
      - DB_PASSWORD=helpdesk_password
      - DB_NAME=helpdesk
      - JWT_SECRET=your-super-secret-jwt-key-change-in-production
      - PORT=3000
    networks:
      - helpdesk-network
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (Nginx para servir arquivos estáticos)
  frontend:
    image: nginx:alpine
    container_name: helpdesk-frontend
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend/dist:/usr/share/nginx/html
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
    networks:
      - helpdesk-network
    restart: unless-stopped

  # Banco de dados MySQL
  mysql:
    image: mysql:8.0
    container_name: helpdesk-mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root_password_change_me
      - MYSQL_DATABASE=helpdesk
      - MYSQL_USER=helpdesk_user
      - MYSQL_PASSWORD=helpdesk_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - ./my.cnf:/etc/mysql/conf.d/my.cnf
    networks:
      - helpdesk-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 30s
      timeout: 10s
      retries: 5

  # Redis para cache/sessões (opcional)
  redis:
    image: redis:7-alpine
    container_name: helpdesk-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - helpdesk-network
    restart: unless-stopped
    command: redis-server --appendonly yes

networks:
  helpdesk-network:
    driver: bridge

volumes:
  mysql_data:
    driver: local
  redis_data:
    driver: local
```

### nginx.conf
```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    # Logs
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Backend upstream
    upstream backend {
        server backend:3000;
    }

    # HTTP Server
    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header Referrer-Policy "no-referrer-when-downgrade" always;
        add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

        # Frontend
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }

        # API proxy
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://backend/health;
        }
    }
}
```

## ☸️ Kubernetes

### namespace.yaml
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: helpdesk
  labels:
    name: helpdesk
```

### mysql-deployment.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: mysql-config
  namespace: helpdesk
data:
  my.cnf: |
    [mysqld]
    default_authentication_plugin=mysql_native_password
    character-set-server=utf8mb4
    collation-server=utf8mb4_unicode_ci
    max_connections=200

---
apiVersion: v1
kind: Secret
metadata:
  name: mysql-secret
  namespace: helpdesk
type: Opaque
data:
  root-password: cm9vdF9wYXNzd29yZA== # root_password (base64)
  user-password: aGVscGRlc2tfcGFzc3dvcmQ= # helpdesk_password (base64)

---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pvc
  namespace: helpdesk
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  namespace: helpdesk
spec:
  replicas: 1
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:8.0
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: root-password
        - name: MYSQL_DATABASE
          value: helpdesk
        - name: MYSQL_USER
          value: helpdesk_user
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: user-password
        ports:
        - containerPort: 3306
        volumeMounts:
        - name: mysql-storage
          mountPath: /var/lib/mysql
        - name: mysql-config
          mountPath: /etc/mysql/conf.d
        livenessProbe:
          exec:
            command:
            - mysqladmin
            - ping
            - -h
            - localhost
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          exec:
            command:
            - mysqladmin
            - ping
            - -h
            - localhost
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: mysql-storage
        persistentVolumeClaim:
          claimName: mysql-pvc
      - name: mysql-config
        configMap:
          name: mysql-config

---
apiVersion: v1
kind: Service
metadata:
  name: mysql-service
  namespace: helpdesk
spec:
  selector:
    app: mysql
  ports:
  - port: 3306
    targetPort: 3306
  type: ClusterIP
```

### app-deployment.yaml
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: helpdesk
data:
  NODE_ENV: "production"
  DB_HOST: "mysql-service"
  DB_USER: "helpdesk_user"
  DB_NAME: "helpdesk"
  PORT: "3000"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
  namespace: helpdesk
type: Opaque
data:
  db-password: aGVscGRlc2tfcGFzc3dvcmQ= # helpdesk_password (base64)
  jwt-secret: eW91ci1zdXBlci1zZWNyZXQtand0LWtleQ== # your-super-secret-jwt-key (base64)

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: helpdesk-app
  namespace: helpdesk
spec:
  replicas: 3
  selector:
    matchLabels:
      app: helpdesk-app
  template:
    metadata:
      labels:
        app: helpdesk-app
    spec:
      containers:
      - name: helpdesk-app
        image: helpdesk-app:latest
        imagePullPolicy: Always
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: NODE_ENV
        - name: DB_HOST
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_HOST
        - name: DB_USER
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_USER
        - name: DB_NAME
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: DB_NAME
        - name: PORT
          valueFrom:
            configMapKeyRef:
              name: app-config
              key: PORT
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: db-password
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"

---
apiVersion: v1
kind: Service
metadata:
  name: helpdesk-service
  namespace: helpdesk
spec:
  selector:
    app: helpdesk-app
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer

---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: helpdesk-ingress
  namespace: helpdesk
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - helpdesk.suaempresa.com
    secretName: helpdesk-tls
  rules:
  - host: helpdesk.suaempresa.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: helpdesk-service
            port:
              number: 80
```

### HorizontalPodAutoscaler
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: helpdesk-hpa
  namespace: helpdesk
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: helpdesk-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

## 🚀 Jenkins Pipeline

### Jenkinsfile
```groovy
pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'your-registry.com'
        APP_NAME = 'helpdesk-app'
        K8S_NAMESPACE = 'helpdesk'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            parallel {
                stage('Backend Dependencies') {
                    steps {
                        dir('backend') {
                            sh 'npm ci'
                        }
                    }
                }
                stage('Frontend Dependencies') {
                    steps {
                        sh 'npm ci'
                    }
                }
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('Backend Tests') {
                    steps {
                        dir('backend') {
                            sh 'npm run test'
                            publishTestResults([
                                testResultsPattern: 'test-results.xml'
                            ])
                        }
                    }
                }
                stage('Frontend Tests') {
                    steps {
                        sh 'npm run test'
                    }
                }
            }
        }
        
        stage('Code Quality') {
            steps {
                sh 'npm run lint'
                
                // SonarQube analysis
                withSonarQubeEnv('SonarQube') {
                    sh '''
                        sonar-scanner \
                        -Dsonar.projectKey=helpdesk-app \
                        -Dsonar.sources=. \
                        -Dsonar.host.url=$SONAR_HOST_URL \
                        -Dsonar.login=$SONAR_AUTH_TOKEN
                    '''
                }
            }
        }
        
        stage('Build') {
            parallel {
                stage('Build Frontend') {
                    steps {
                        sh 'npm run build'
                        archiveArtifacts artifacts: 'dist/**', fingerprint: true
                    }
                }
                stage('Build Docker Image') {
                    steps {
                        dir('backend') {
                            script {
                                def image = docker.build("${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}")
                                docker.withRegistry("https://${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                                    image.push()
                                    image.push('latest')
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                // Trivy security scan
                sh """
                    trivy image --exit-code 0 --severity HIGH,CRITICAL \
                    --format json -o trivy-report.json \
                    ${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER}
                """
                
                archiveArtifacts artifacts: 'trivy-report.json', fingerprint: true
            }
        }
        
        stage('Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                script {
                    sh """
                        kubectl set image deployment/helpdesk-app \
                        helpdesk-app=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} \
                        -n ${K8S_NAMESPACE}-staging
                        
                        kubectl rollout status deployment/helpdesk-app \
                        -n ${K8S_NAMESPACE}-staging --timeout=300s
                    """
                }
            }
        }
        
        stage('Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
                
                script {
                    sh """
                        kubectl set image deployment/helpdesk-app \
                        helpdesk-app=${DOCKER_REGISTRY}/${APP_NAME}:${BUILD_NUMBER} \
                        -n ${K8S_NAMESPACE}
                        
                        kubectl rollout status deployment/helpdesk-app \
                        -n ${K8S_NAMESPACE} --timeout=300s
                    """
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        
        success {
            slackSend(
                color: 'good',
                message: "✅ Pipeline executado com sucesso para ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
        
        failure {
            slackSend(
                color: 'danger',
                message: "❌ Pipeline falhou para ${env.JOB_NAME} - ${env.BUILD_NUMBER}"
            )
        }
    }
}
```

## 📊 Monitoramento

### Prometheus Configuration
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: helpdesk
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    
    scrape_configs:
    - job_name: 'helpdesk-app'
      static_configs:
      - targets: ['helpdesk-service:80']
      metrics_path: /metrics
      
    - job_name: 'mysql'
      static_configs:
      - targets: ['mysql-service:3306']
```

### Grafana Dashboard
```json
{
  "dashboard": {
    "title": "HelpDesk Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))"
          }
        ]
      }
    ]
  }
}
```

Este conjunto completo de configurações Docker e DevOps fornece:
- ✅ Containerização completa
- ✅ Orquestração Kubernetes
- ✅ Pipeline CI/CD automatizado
- ✅ Monitoramento e observabilidade
- ✅ Segurança e qualidade de código
- ✅ Escalabilidade automática
