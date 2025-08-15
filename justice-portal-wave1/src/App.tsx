import AccessGate from "./routes/AccessGate";
import Exhibits from "./routes/Exhibits";
import Viewer from "./routes/Viewer";
import Front from "./routes/Front";
import { useEffect, useState } from "react";
import { ConfirmationProvider } from "./contexts/ConfirmationContext";
function useRoute() {
  const [route, setRoute] = useState<string>(location.hash || "#/");
  useEffect(() => {
    const on = () => setRoute(location.hash || "#/");
    addEventListener("hashchange", on);
    return () => removeEventListener("hashchange", on)
  }, []);
  return route;
}

function RouterView() {
  const route = useRoute();
  if (route.startsWith("#/front")) return <Front />;
  if (route.startsWith("#/viewer/")) return <Viewer />;
  if (route.startsWith("#/exhibits")) return <Exhibits />;
  // Default: redirect to front matter
  location.hash = "#/front";
  return null;
}

export default function App() {
  return (
    <ConfirmationProvider>
      <AccessGate>
        <RouterView />
      </AccessGate>
    </ConfirmationProvider>
  );
}
