import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import org.eclipse.microprofile.openapi.annotations.Operation;

@Path("/docs")
public class DocsResource {

    private static final String PAGE = """
            <!doctype html>
            <html>
              <head>
                <meta charset="utf-8">
                <title>Price API</title>
                <script type="module" src="https://unpkg.com/rapidoc@9.3.8/dist/rapidoc-min.js"></script>
              </head>
              <body>
                <rapi-doc
                  spec-url="/q/openapi?format=json"
                  server-url="http://localhost:8080"
                  theme="dark"
                  render-style="focused"
                  show-header="false"
                  allow-server-selection="false">
                </rapi-doc>
              </body>
            </html>
            """;

    @GET
    @Produces(MediaType.TEXT_HTML)
    @Operation(hidden = true)
    public String page() {
        return PAGE;
    }
}
