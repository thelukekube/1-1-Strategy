import data
import strat_logic

# -------------------------------------------------------- TRADE EXECUTION ----------------------------------------------------------

# ENTER POZICE - POKUD BUY - OTEVŘENÍ NA HIGH PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
                    # POKUD SELL - OTEVŘENÍ NA LOW PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
        
        # STOP LOSS - POKUD BUY - STOP LOSS O 1 PIP POD LOW PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)  
                    # POKUD SELL - STOP LOSS O 1 PIP NAD HIGH PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)

        # TAKE PROFIT - zatím neřešit