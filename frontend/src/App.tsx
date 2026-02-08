import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import { isAuthenticated } from './services/auth';

// 認証が必要なページを保護するコンポーネント
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  return isAuthenticated() ? <>{children}</> : <Navigate to="/login" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* ログインページ */}
        <Route path="/login" element={<Login />} />
        
        {/* ホームページ（仮）- 認証が必要 */}
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
        
        {/* その他のパスは全てログインページへ */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;