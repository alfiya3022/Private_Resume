import { useState } from "react";
import { getApiHealth } from "./api";

function App() {
  const [status, setStatus] = useState("Not checked yet");
  const [loading, setLoading] = useState(false);

  async function checkApi() {
    setLoading(true);
    setStatus("Connecting to backend...");

    try {
      const result = await getApiHealth();
      setStatus(`Backend response: ${result.status}`);
    } catch (error) {
      setStatus(`Connection failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-stone-100 px-6 py-16 text-stone-900">
      <section className="mx-auto max-w-2xl rounded-2xl border border-stone-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-medium uppercase tracking-widest text-orange-600">
          PrivateResume · E00
        </p>

        <h1 className="mt-4 text-3xl font-bold">Frontend ↔ Backend</h1>

        <p className="mt-3 text-stone-600">
          Verify that the React frontend can communicate with the FastAPI
          backend.
        </p>

        <button
          onClick={checkApi}
          disabled={loading}
          className="mt-6 rounded-lg bg-orange-600 px-5 py-3 font-medium text-white hover:bg-orange-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? "Checking..." : "Check backend connection"}
        </button>

        <p role="status" className="mt-5 rounded-lg bg-stone-100 p-4 text-sm">
          {status}
        </p>
      </section>
    </main>
  );
}

export default App;
