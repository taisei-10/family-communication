import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import FamilySetup from './pages/FamilySetup';
import { isAuthenticated } from './services/auth';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  return isAuthenticated() ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* 家族セットアップページ */}
        <Route 
          path="/family/setup" 
          element={
            <ProtectedRoute>
              <FamilySetup />
            </ProtectedRoute>
          } 
        />
        
        {/* ホームページ */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <div className="p-8">
                <h1 className="text-2xl font-bold">ホームページ</h1>
                <p>ログイン成功！</p>
              </div>
            </ProtectedRoute>
          } 
        />
        
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;