import QueryContext from "./lib/query-client";
import Router from "./lib/router";

function App() {
  return (
    <QueryContext>
      <Router />
    </QueryContext>
  );
}

export default App;
