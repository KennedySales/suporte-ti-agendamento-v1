
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Calendar, Clock, User, Shield, CheckCircle } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

const Index = () => {
  const [currentView, setCurrentView] = useState<'home' | 'login' | 'agendamento'>('home');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState<{nome: string, email: string} | null>(null);
  const { toast } = useToast();

  // Login form state
  const [loginData, setLoginData] = useState({
    email: '',
    senha: ''
  });

  // Agendamento form state
  const [agendamentoData, setAgendamentoData] = useState({
    data: '',
    hora: '',
    descricao: ''
  });

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Tentativa de login:', loginData);
    
    // Simulação de autenticação (em produção seria uma chamada à API)
    if (loginData.email === 'admin@empresa.com' && loginData.senha === '123456') {
      setIsLoggedIn(true);
      setUser({ nome: 'Administrador', email: loginData.email });
      setCurrentView('agendamento');
      toast({
        title: "Login realizado com sucesso!",
        description: "Bem-vindo ao sistema de suporte técnico.",
      });
    } else {
      toast({
        title: "Erro no login",
        description: "Email ou senha incorretos.",
        variant: "destructive",
      });
    }
  };

  const handleAgendamento = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Dados do agendamento:', agendamentoData);
    
    // Simulação de salvamento (em produção seria uma chamada à API)
    toast({
      title: "Agendamento realizado!",
      description: `Seu atendimento foi agendado para ${agendamentoData.data} às ${agendamentoData.hora}.`,
    });
    
    // Reset form
    setAgendamentoData({
      data: '',
      hora: '',
      descricao: ''
    });
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUser(null);
    setCurrentView('home');
    setLoginData({ email: '', senha: '' });
    toast({
      title: "Logout realizado",
      description: "Até logo!",
    });
  };

  if (currentView === 'home') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <Shield className="h-8 w-8 text-blue-600 mr-3" />
                <h1 className="text-2xl font-bold text-gray-900">HelpDesk Pro</h1>
              </div>
              <Button onClick={() => setCurrentView('login')} className="bg-blue-600 hover:bg-blue-700">
                Acessar Sistema
              </Button>
            </div>
          </div>
        </header>

        {/* Hero Section */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Sistema de Suporte Técnico em TI
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Agende seus atendimentos técnicos de forma rápida e eficiente. 
              Nossa equipe está pronta para resolver seus problemas de TI.
            </p>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Calendar className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                <CardTitle>Agendamento Fácil</CardTitle>
                <CardDescription>
                  Agende seus atendimentos técnicos em poucos cliques
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Clock className="h-12 w-12 text-green-600 mx-auto mb-4" />
                <CardTitle>Atendimento Rápido</CardTitle>
                <CardDescription>
                  Resolução ágil dos seus problemas de TI
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <User className="h-12 w-12 text-purple-600 mx-auto mb-4" />
                <CardTitle>Suporte Especializado</CardTitle>
                <CardDescription>
                  Técnicos qualificados para todas as suas necessidades
                </CardDescription>
              </CardHeader>
            </Card>
          </div>

          {/* CTA Section */}
          <div className="bg-white rounded-2xl shadow-xl p-8 text-center">
            <h3 className="text-2xl font-bold text-gray-900 mb-4">
              Pronto para começar?
            </h3>
            <p className="text-gray-600 mb-6">
              Acesse o sistema e agende seu próximo atendimento técnico
            </p>
            <Button 
              onClick={() => setCurrentView('login')} 
              size="lg"
              className="bg-blue-600 hover:bg-blue-700"
            >
              Fazer Login
            </Button>
          </div>
        </main>

        {/* Footer */}
        <footer className="bg-gray-900 text-white py-8 mt-16">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p>&copy; 2024 HelpDesk Pro. Sistema de Suporte Técnico em TI.</p>
          </div>
        </footer>
      </div>
    );
  }

  if (currentView === 'login') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="space-y-1">
            <div className="flex items-center justify-center mb-4">
              <Shield className="h-10 w-10 text-blue-600" />
            </div>
            <CardTitle className="text-2xl text-center">Login</CardTitle>
            <CardDescription className="text-center">
              Acesse o sistema de suporte técnico
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleLogin} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="seu@email.com"
                  value={loginData.email}
                  onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="senha">Senha</Label>
                <Input
                  id="senha"
                  type="password"
                  placeholder="Digite sua senha"
                  value={loginData.senha}
                  onChange={(e) => setLoginData({...loginData, senha: e.target.value})}
                  required
                />
              </div>
              <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">
                Entrar
              </Button>
            </form>
            
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-700 font-medium">Dados para teste:</p>
              <p className="text-sm text-blue-600">Email: admin@empresa.com</p>
              <p className="text-sm text-blue-600">Senha: 123456</p>
            </div>
            
            <div className="mt-4 text-center">
              <Button 
                variant="ghost" 
                onClick={() => setCurrentView('home')}
                className="text-gray-600 hover:text-gray-800"
              >
                ← Voltar ao início
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (currentView === 'agendamento') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-6">
              <div className="flex items-center">
                <Shield className="h-8 w-8 text-blue-600 mr-3" />
                <h1 className="text-2xl font-bold text-gray-900">HelpDesk Pro</h1>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-gray-700">Olá, {user?.nome}</span>
                <Button onClick={handleLogout} variant="outline">
                  Sair
                </Button>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Agendar Atendimento Técnico
            </h2>
            <p className="text-gray-600">
              Preencha o formulário abaixo para agendar seu atendimento
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Formulário de Agendamento */}
            <Card>
              <CardHeader>
                <CardTitle>Dados do Agendamento</CardTitle>
                <CardDescription>
                  Informe os detalhes do seu atendimento técnico
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleAgendamento} className="space-y-6">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label htmlFor="data">Data</Label>
                      <Input
                        id="data"
                        type="date"
                        value={agendamentoData.data}
                        onChange={(e) => setAgendamentoData({...agendamentoData, data: e.target.value})}
                        required
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="hora">Hora</Label>
                      <Input
                        id="hora"
                        type="time"
                        value={agendamentoData.hora}
                        onChange={(e) => setAgendamentoData({...agendamentoData, hora: e.target.value})}
                        required
                      />
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <Label htmlFor="descricao">Descrição do Problema</Label>
                    <Textarea
                      id="descricao"
                      placeholder="Descreva detalhadamente o problema que precisa ser resolvido..."
                      value={agendamentoData.descricao}
                      onChange={(e) => setAgendamentoData({...agendamentoData, descricao: e.target.value})}
                      rows={4}
                      required
                    />
                  </div>

                  <Button type="submit" className="w-full bg-green-600 hover:bg-green-700">
                    <CheckCircle className="w-4 h-4 mr-2" />
                    Confirmar Agendamento
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Informações Adicionais */}
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Horários de Atendimento</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="font-medium">Segunda a Sexta:</span>
                    <span>08:00 - 18:00</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Sábado:</span>
                    <span>08:00 - 12:00</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="font-medium">Domingo:</span>
                    <span>Fechado</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Tipos de Atendimento</CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Instalação de Software</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Manutenção de Hardware</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Configuração de Rede</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Suporte Remoto</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-4 h-4 text-green-600" />
                    <span>Backup e Recuperação</span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Contato de Emergência</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-600 mb-2">
                    Para situações urgentes fora do horário comercial:
                  </p>
                  <p className="font-medium">📞 (11) 9999-9999</p>
                  <p className="font-medium">📧 emergencia@helpdesk.com</p>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    );
  }

  return null;
};

export default Index;
