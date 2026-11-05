import jakarta.inject.Inject;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.QueryParam;
import jakarta.ws.rs.core.MediaType;
import java.util.List;

@Path("/total")
public class PriceResource {

    @Inject
    PriceService priceService;

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public double total(@QueryParam("prices") List<Integer> prices, @QueryParam("discount") int discount) {
        return priceService.total(prices, discount);
    }
}
