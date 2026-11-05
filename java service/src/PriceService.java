import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class PriceService {

    public double total(List<Integer> prices, int discountPercent) {
        int subtotal = 0;
        for (int price : prices) {
            subtotal += price;
        }

        double discount = subtotal * (discountPercent / 100);
        return subtotal - discount;
    }
}
