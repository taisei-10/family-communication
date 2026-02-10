import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createFamily, joinFamilyByInviteCode } from '../services/family';

/**
 * 家族グループのセットアップページ
 * 新規作成または既存グループへの参加
 */
function FamilySetup() {
  const navigate = useNavigate();

  // タブの状態（'create' または 'join'）
  const [mode, setMode] = useState<'create' | 'join'>('create');
  
  // 作成モードの入力値
  const [familyName, setFamilyName] = useState('');
  
  // 参加モードの入力値（招待コード）
  const [inviteCode, setInviteCode] = useState('');
  
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [createdFamily, setCreatedFamily] = useState<any>(null);

  /**
   * 家族グループを新規作成
   */
  const handleCreate = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    console.log('[FAMILY SETUP] 家族作成試行:', { familyName });

    try {
      const family = await createFamily({ name: familyName });
      console.log('[FAMILY SETUP] 家族作成成功:', family);
      
      // 作成した家族情報を保存（招待コード表示用）
      setCreatedFamily(family);
    } catch (err: any) {
      console.error('[FAMILY SETUP] 家族作成失敗:', err);
      const errorMessage = err.response?.data?.detail || err.message || '家族の作成に失敗しました';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 既存の家族グループに参加
   */
  const handleJoin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    console.log('[FAMILY SETUP] 家族参加試行:', { inviteCode });

    try {
      const family = await joinFamilyByInviteCode(inviteCode);
      console.log('[FAMILY SETUP] 家族参加成功:', family);
      
      // ホームページへ遷移
      navigate('/');
    } catch (err: any) {
      console.error('[FAMILY SETUP] 家族参加失敗:', err);
      const errorMessage = err.response?.data?.detail || err.message || '家族への参加に失敗しました';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '500px', margin: '50px auto', padding: '20px' }}>
      <h2>家族グループのセットアップ</h2>
      <p style={{ color: '#666', marginBottom: '30px' }}>
        家族グループを作成するか、既存のグループに参加してください
      </p>

      {/* タブ切り替え */}
      <div style={{ display: 'flex', marginBottom: '20px', borderBottom: '1px solid #ddd' }}>
        <button
          onClick={() => {
            setMode('create');
            setError('');
          }}
          style={{
            flex: 1,
            padding: '10px',
            border: 'none',
            backgroundColor: 'transparent',
            borderBottom: mode === 'create' ? '2px solid #1976d2' : 'none',
            color: mode === 'create' ? '#1976d2' : '#666',
            fontWeight: mode === 'create' ? 'bold' : 'normal',
            cursor: 'pointer',
          }}
        >
          家族を作る
        </button>
        <button
          onClick={() => {
            setMode('join');
            setError('');
          }}
          style={{
            flex: 1,
            padding: '10px',
            border: 'none',
            backgroundColor: 'transparent',
            borderBottom: mode === 'join' ? '2px solid #1976d2' : 'none',
            color: mode === 'join' ? '#1976d2' : '#666',
            fontWeight: mode === 'join' ? 'bold' : 'normal',
            cursor: 'pointer',
          }}
        >
          家族に参加
        </button>
      </div>

      {/* エラーメッセージ */}
      {error && (
        <div style={{
          padding: '10px',
          backgroundColor: '#ffebee',
          color: '#c62828',
          borderRadius: '4px',
          marginBottom: '20px',
        }}>
          {error}
        </div>
      )}

      {/* 家族を作るフォーム */}
      {mode === 'create' && !createdFamily && (
        <form onSubmit={handleCreate}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              家族グループ名
            </label>
            <input
              type="text"
              value={familyName}
              onChange={(e) => setFamilyName(e.target.value)}
              placeholder="例: 山田家"
              required
              style={{
                width: '100%',
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '4px',
              }}
            />
            <small style={{ color: '#666', fontSize: '12px' }}>
              家族メンバーが識別しやすい名前をつけてください
            </small>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: loading ? '#ccc' : '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
            }}
          >
            {loading ? '作成中...' : '家族グループを作成'}
          </button>
        </form>
      )}

      {/* 作成成功メッセージと招待コード表示 */}
      {mode === 'create' && createdFamily && (
        <div>
          <div style={{
            padding: '20px',
            backgroundColor: '#e8f5e9',
            borderRadius: '8px',
            marginBottom: '20px',
          }}>
            <h3 style={{ margin: '0 0 10px 0', color: '#2e7d32' }}>✓ 家族グループを作成しました！</h3>
            <p style={{ margin: '0 0 15px 0', fontSize: '14px', color: '#666' }}>
              家族名: <strong>{createdFamily.name}</strong>
            </p>
            <div style={{
              padding: '15px',
              backgroundColor: 'white',
              borderRadius: '4px',
              border: '2px dashed #4caf50',
            }}>
              <label style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold' }}>
                招待コード
              </label>
              <div style={{
                fontSize: '24px',
                fontFamily: 'monospace',
                color: '#1976d2',
                letterSpacing: '2px',
                userSelect: 'all',
              }}>
                {createdFamily.invite_code}
              </div>
              <small style={{ color: '#666', fontSize: '12px', marginTop: '5px', display: 'block' }}>
                このコードを家族メンバーに共有してください
              </small>
            </div>
          </div>
          <button
            onClick={() => navigate('/')}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontWeight: 'bold',
            }}
          >
            ホームへ
          </button>
        </div>
      )}

      {/* 家族に参加フォーム */}
      {mode === 'join' && (
        <form onSubmit={handleJoin}>
          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px' }}>
              招待コード
            </label>
            <input
              type="text"
              value={inviteCode}
              onChange={(e) => setInviteCode(e.target.value)}
              placeholder="招待コードを入力"
              required
              style={{
                width: '100%',
                padding: '8px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                fontFamily: 'monospace',
                fontSize: '16px',
                letterSpacing: '1px',
              }}
            />
            <small style={{ color: '#666', fontSize: '12px' }}>
              家族メンバーから共有された招待コードを入力してください
            </small>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '10px',
              backgroundColor: loading ? '#ccc' : '#1976d2',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: loading ? 'not-allowed' : 'pointer',
              fontWeight: 'bold',
            }}
          >
            {loading ? '参加中...' : '家族グループに参加'}
          </button>
        </form>
      )}
    </div>
  );
}

export default FamilySetup;