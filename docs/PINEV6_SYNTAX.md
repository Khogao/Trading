# Pine Script v6: Official Reference Manual (Community Sourced)

This document contains a comprehensive list of variables, constants, and functions available in Pine Script v6, based on community-sourced documentation. This is the full, unfiltered output retrieved from the source.

## Variables & Functions

### ask

- **Type:** `series float`
- **Description:** The ask price at the time of the current tick, which represents the lowest price an active seller will accept for the instrument at its current value. This information is available only on the "1T" timeframe. On other timeframes, the variable's value is na.

### bar_index

- **Type:** `series int`
- **Description:** Current bar index. Numbering is zero-based, index of the first bar is 0.

### barstate.isconfirmed

- **Type:** `series bool`
- **Description:** Returns true if the script is calculating the last (closing) update of the current bar. The next script calculation will be on the new bar data.

### barstate.isfirst

- **Type:** `series bool`
- **Description:** Returns true if current bar is first bar in barset, false otherwise.

### barstate.ishistory

- **Type:** `series bool`
- **Description:** Returns true if current bar is a historical bar, false otherwise.

### barstate.islast

- **Type:** `series bool`
- **Description:** Returns true if current bar is the last bar in barset, false otherwise. This condition is true for all real-time bars in barset.

### barstate.islastconfirmedhistory

- **Type:** `series bool`
- **Description:** Returns true if script is executing on the dataset's last bar when market is closed, or script is executing on the bar immediately preceding the real-time bar, if market is open. Returns false otherwise.

### barstate.isnew

- **Type:** `series bool`
- **Description:** Returns true if script is currently calculating on new bar, false otherwise. This variable is true when calculating on historical bars or on first update of a newly generated real-time bar.

### barstate.isrealtime

- **Type:** `series bool`
- **Description:** Returns true if current bar is a real-time bar, false otherwise.

### bid

- **Type:** `series float`
- **Description:** The bid price at the time of the current tick, which represents the highest price an active buyer is willing to pay for the instrument at its current value. This information is available only on the "1T" timeframe. On other timeframes, the variable's value is na.

### box.all

- **Type:** `array`
- **Description:** Returns an array filled with all the current boxes drawn by the script.

### chart.bg_color

- **Type:** `input color`
- **Description:** Returns the color of the chart's background from the "Chart settings/Appearance/Background" field. When a gradient is selected, the middle point of the gradient is returned.

### chart.fg_color

- **Type:** `input color`
- **Description:** Returns a color providing optimal contrast with chart.bg_color.

### chart.is_heikinashi

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Heikin Ashi, false otherwise.

### chart.is_kagi

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Kagi, false otherwise.

### chart.is_linebreak

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Line break, false otherwise.

### chart.is_pnf

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Point & figure, false otherwise.

### chart.is_range

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Range, false otherwise.

### chart.is_renko

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is Renko, false otherwise.

### chart.is_standard

- **Type:** `simple bool`
- **Description:** Returns true if the chart type is not one of the following: Renko, Kagi, Line break, Point & figure, Range, Heikin Ashi; false otherwise.

### chart.left_visible_bar_time

- **Type:** `input int`
- **Description:** The time of the leftmost bar currently visible on the chart.

### chart.right_visible_bar_time

- **Type:** `input int`
- **Description:** The time of the rightmost bar currently visible on the chart.

### close

- **Type:** `series float`
- **Description:** Close price of the current bar when it has closed, or last traded price of a yet incomplete, realtime bar.

### dayofmonth

- **Type:** `series int`
- **Description:** Date of current bar time in exchange timezone.

### dayofweek

- **Type:** `series int`
- **Description:** Day of week for current bar time in exchange timezone.

### dividends.future_amount

- **Type:** `series float`
- **Description:** Returns the payment amount of the upcoming dividend in the currency of the current instrument, or na if this data isn't available.

### dividends.future_ex_date

- **Type:** `series int`
- **Description:** Returns the Ex-dividend date (Ex-date) of the current instrument's next dividend payment, or na if this data isn't available. Ex-dividend date signifies when investors are no longer entitled to a payout from the most recent dividend. Only those who purchased shares before this day are entitled to the dividend payment.

### dividends.future_pay_date

- **Type:** `series int`
- **Description:** Returns the Payment date (Pay date) of the current instrument's next dividend payment, or na if this data isn't available. Payment date signifies the day when eligible investors will receive the dividend payment.

### earnings.future_eps

- **Type:** `series float`
- **Description:** Returns the estimated Earnings per Share of the next earnings report in the currency of the instrument, or na if this data isn't available.

### earnings.future_period_end_time

- **Type:** `series int`
- **Description:** Checks the data for the next earnings report and returns the UNIX timestamp of the day when the financial period covered by those earnings ends, or na if this data isn't available.

### earnings.future_revenue

- **Type:** `series float`
- **Description:** Returns the estimated Revenue of the next earnings report in the currency of the instrument, or na if this data isn't available.

### earnings.future_time

- **Type:** `series int`
- **Description:** Returns a UNIX timestamp indicating the expected time of the next earnings report, or na if this data isn't available.

### high

- **Type:** `series float`
- **Description:** Current high price.

### hl2

- **Type:** `series float`
- **Description:** Is a shortcut for (high + low)/2

### hlc3

- **Type:** `series float`
- **Description:** Is a shortcut for (high + low + close)/3

### hlcc4

- **Type:** `series float`
- **Description:** Is a shortcut for (high + low + close + close)/4

### hour

- **Type:** `series int`
- **Description:** Current bar hour in exchange timezone.

### label.all

- **Type:** `array`
- **Description:** Returns an array filled with all the current labels drawn by the script.

### last_bar_index

- **Type:** `series int`
- **Description:** Bar index of the last chart bar. Bar indices begin at zero on the first bar.

### last_bar_time

- **Type:** `series int`
- **Description:** Time in UNIX format of the last chart bar. It is the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970.

### line.all

- **Type:** `array`
- **Description:** Returns an array filled with all the current lines drawn by the script.

### linefill.all

- **Type:** `array`
- **Description:** Returns an array filled with all the current linefill objects drawn by the script.

### low

- **Type:** `series float`
- **Description:** Current low price.

### minute

- **Type:** `series int`
- **Description:** Current bar minute in exchange timezone.

### month

- **Type:** `series int`
- **Description:** Current bar month in exchange timezone.

### na

- **Type:** `simple na`
- **Description:** A keyword signifying "not available", indicating that a variable has no assigned value.

### ohlc4

- **Type:** `series float`
- **Description:** Is a shortcut for (open + high + low + close)/4

### open

- **Type:** `series float`
- **Description:** Current open price.

### polyline.all

- **Type:** `array`
- **Description:** Returns an array containing all current polyline instances drawn by the script.

### second

- **Type:** `series int`
- **Description:** Current bar second in exchange timezone.

### session.isfirstbar

- **Type:** `series bool`
- **Description:** Returns true if the current bar is the first bar of the day's session, false otherwise. If extended session information is used, only returns true on the first bar of the pre-market bars.

### session.isfirstbar_regular

- **Type:** `series bool`
- **Description:** Returns true on the first regular session bar of the day, false otherwise. The result is the same whether extended session information is used or not.

### session.islastbar

- **Type:** `series bool`
- **Description:** Returns true if the current bar is the last bar of the day's session, false otherwise. If extended session information is used, only returns true on the last bar of the post-market bars.

### session.islastbar_regular

- **Type:** `series bool`
- **Description:** Returns true on the last regular session bar of the day, false otherwise. The result is the same whether extended session information is used or not.

### session.ismarket

- **Type:** `series bool`
- **Description:** Returns true if the current bar is a part of the regular trading hours (i.e. market hours), false otherwise.

### session.ispostmarket

- **Type:** `series bool`
- **Description:** Returns true if the current bar is a part of the post-market, false otherwise. On non-intraday charts always returns false.

### session.ispremarket

- **Type:** `series bool`
- **Description:** Returns true if the current bar is a part of the pre-market, false otherwise. On non-intraday charts always returns false.

### strategy.account_currency

- **Type:** `simple string`
- **Description:** Returns the currency used to calculate results, which can be set in the strategy's properties.

### strategy.avg_losing_trade

- **Type:** `series float`
- **Description:** Returns the average amount of money lost per losing trade. Calculated as the sum of losses divided by the number of losing trades.

### strategy.avg_losing_trade_percent

- **Type:** `series float`
- **Description:** Returns the average percentage loss per losing trade. Calculated as the sum of loss percentages divided by the number of losing trades.

### strategy.avg_trade

- **Type:** `series float`
- **Description:** Returns the average amount of money gained or lost per trade. Calculated as the sum of all profits and losses divided by the number of closed trades.

### strategy.avg_trade_percent

- **Type:** `series float`
- **Description:** Returns the average percentage gain or loss per trade. Calculated as the sum of all profit and loss percentages divided by the number of closed trades.

### strategy.avg_winning_trade

- **Type:** `series float`
- **Description:** Returns the average amount of money gained per winning trade. Calculated as the sum of profits divided by the number of winning trades.

### strategy.avg_winning_trade_percent

- **Type:** `series float`
- **Description:** Returns the average percentage gain per winning trade. Calculated as the sum of profit percentages divided by the number of winning trades.

### strategy.closedtrades

- **Type:** `series int`
- **Description:** Number of trades, which were closed for the whole trading range.

### strategy.closedtrades.first_index

- **Type:** `series int`
- **Description:** The index, or trade number, of the first (oldest) trade listed in the List of Trades. This number is usually zero. If more trades than the allowed limit have been closed, the oldest trades are removed, and this number is the index of the oldest remaining trade.

### strategy.equity

- **Type:** `series float`
- **Description:** Current equity (strategy.initial_capital + strategy.netprofit + strategy.openprofit).

### strategy.eventrades

- **Type:** `series int`
- **Description:** Number of breakeven trades for the whole trading range.

### strategy.grossloss

- **Type:** `series float`
- **Description:** Total currency value of all completed losing trades.

### strategy.grossloss_percent

- **Type:** `series float`
- **Description:** The total value of all completed losing trades, expressed as a percentage of the initial capital.

### strategy.grossprofit

- **Type:** `series float`
- **Description:** Total currency value of all completed winning trades.

### strategy.grossprofit_percent

- **Type:** `series float`
- **Description:** The total currency value of all completed winning trades, expressed as a percentage of the initial capital.

### strategy.initial_capital

- **Type:** `series float`
- **Description:** The amount of initial capital set in the strategy properties.

### strategy.losstrades

- **Type:** `series int`
- **Description:** Number of unprofitable trades for the whole trading range.

### strategy.margin_liquidation_price

- **Type:** `series float`
- **Description:** When margin is used in a strategy, returns the price point where a simulated margin call will occur and liquidate enough of the position to meet the margin requirements.

### strategy.max_contracts_held_all

- **Type:** `series float`
- **Description:** Maximum number of contracts/shares/lots/units in one trade for the whole trading range.

### strategy.max_contracts_held_long

- **Type:** `series float`
- **Description:** Maximum number of contracts/shares/lots/units in one long trade for the whole trading range.

### strategy.max_contracts_held_short

- **Type:** `series float`
- **Description:** Maximum number of contracts/shares/lots/units in one short trade for the whole trading range.

### strategy.max_drawdown

- **Type:** `series float`
- **Description:** Maximum equity drawdown value for the whole trading range.

### strategy.max_drawdown_percent

- **Type:** `series float`
- **Description:** The maximum equity drawdown value for the whole trading range, expressed as a percentage and calculated by formula: Lowest Value During Trade / (Entry Price x Quantity) * 100.

### strategy.max_runup

- **Type:** `series float`
- **Description:** Maximum equity run-up value for the whole trading range.

### strategy.max_runup_percent

- **Type:** `series float`
- **Description:** The maximum equity run-up value for the whole trading range, expressed as a percentage and calculated by formula: Highest Value During Trade / (Entry Price x Quantity) * 100.

### strategy.netprofit

- **Type:** `series float`
- **Description:** Total currency value of all completed trades.

### strategy.netprofit_percent

- **Type:** `series float`
- **Description:** The total value of all completed trades, expressed as a percentage of the initial capital.

### strategy.openprofit

- **Type:** `series float`
- **Description:** Current unrealized profit or loss for all open positions.

### strategy.openprofit_percent

- **Type:** `series float`
- **Description:** The current unrealized profit or loss for all open positions, expressed as a percentage and calculated by formula: openPL / realizedEquity * 100.

### strategy.opentrades

- **Type:** `series int`
- **Description:** Number of market position entries, which were not closed and remain opened. If there is no open market position, 0 is returned.

### strategy.opentrades.capital_held

- **Type:** `series float`
- **Description:** Returns the capital amount currently held by open trades.

### strategy.position_avg_price

- **Type:** `series float`
- **Description:** Average entry price of current market position. If the market position is flat, 'NaN' is returned.

### strategy.position_entry_name

- **Type:** `series string`
- **Description:** Name of the order that initially opened current market position.

### strategy.position_size

- **Type:** `series float`
- **Description:** Direction and size of the current market position. If the value is > 0, the market position is long. If the value is < 0, the market position is short. The absolute value is the number of contracts/shares/lots/units in trade (position size).

### strategy.wintrades

- **Type:** `series int`
- **Description:** Number of profitable trades for the whole trading range.

### syminfo.basecurrency

- **Type:** `simple string`
- **Description:** Returns a string containing the code representing the symbol's base currency (i.e., the traded currency or coin) if the instrument is a Forex or Crypto pair or a derivative based on such a pair. Otherwise, it returns an empty string. For example, this variable returns "EUR" for "EURJPY", "BTC" for "BTCUSDT", "CAD" for "CME:6C1!", and "" for "NASDAQ:AAPL".

### syminfo.country

- **Type:** `simple string`
- **Description:** Returns the two-letter code of the country where the symbol is traded, in the ISO 3166-1 alpha-2 format, or na if the exchange is not directly tied to a specific country. For example, on "NASDAQ:AAPL" it will return "US", on "LSE:AAPL" it will return "GB", and on "BITSTAMP:BTCUSD it will return na.

### syminfo.currency

- **Type:** `simple string`
- **Description:** Returns a string containing the code representing the currency of the symbol's prices. For example, this variable returns "USD" for "NASDAQ:AAPL" and "JPY" for "EURJPY".

### syminfo.current_contract

- **Type:** `simple string`
- **Description:** The ticker identifier of the underlying contract, if the current symbol is a continuous futures contract; na otherwise.

### syminfo.description

- **Type:** `simple string`
- **Description:** Description for the current symbol.

### syminfo.employees

- **Type:** `simple int`
- **Description:** The number of employees the company has.

### syminfo.expiration_date

- **Type:** `simple int`
- **Description:** A UNIX timestamp representing the start of the last day of the current futures contract. This variable is only compatible with non-continuous futures symbols. On other symbols, it returns na.

### syminfo.industry

- **Type:** `simple string`
- **Description:** Returns the industry of the symbol, or na if the symbol has no industry. Example: "Internet Software/Services", "Packaged software", "Integrated Oil", "Motor Vehicles", etc. These are the same values one can see in the chart's "Symbol info" window.

### syminfo.main_tickerid

- **Type:** `simple string`
- **Description:** A ticker identifier representing the current chart's symbol. The value contains an exchange prefix and a symbol name, separated by a colon (e.g., "NASDAQ:AAPL"). It can also include information about data modifications such as dividend adjustment, non-standard chart type, currency conversion, etc. Unlike syminfo.tickerid, this variable's value does not change when used in the expression argument of a request.*() function call.

### syminfo.mincontract

- **Type:** `simple float`
- **Description:** The smallest amount of the current symbol that can be traded. This limit is set by the exchange. For cryptocurrencies, it is often less than 1 token. For most other types of asset, it is often 1.

### syminfo.minmove

- **Type:** `simple int`
- **Description:** Returns a whole number used to calculate the smallest increment between a symbol's price movements (syminfo.mintick). It is the numerator in the syminfo.mintick formula: syminfo.minmove / syminfo.pricescale = syminfo.mintick.

### syminfo.mintick

- **Type:** `simple float`
- **Description:** Min tick value for the current symbol.

### syminfo.pointvalue

- **Type:** `simple float`
- **Description:** Point value for the current symbol.

### syminfo.prefix

- **Type:** `simple string`
- **Description:** Prefix of current symbol name (i.e. for 'CME_EOD:TICKER' prefix is 'CME_EOD').

### syminfo.pricescale

- **Type:** `simple int`
- **Description:** Returns a whole number used to calculate the smallest increment between a symbol's price movements (syminfo.mintick). It is the denominator in the syminfo.mintick formula: syminfo.minmove / syminfo.pricescale = syminfo.mintick.

### syminfo.recommendations_buy

- **Type:** `series int`
- **Description:** The number of analysts who gave the current symbol a "Buy" rating.

### syminfo.recommendations_buy_strong

- **Type:** `series int`
- **Description:** The number of analysts who gave the current symbol a "Strong Buy" rating.

### syminfo.recommendations_date

- **Type:** `series int`
- **Description:** The starting date of the last set of recommendations for the current symbol.

### syminfo.recommendations_hold

- **Type:** `series int`
- **Description:** The number of analysts who gave the current symbol a "Hold" rating.

### syminfo.recommendations_sell

- **Type:** `series int`
- **Description:** The number of analysts who gave the current symbol a "Sell" rating.

### syminfo.recommendations_sell_strong

- **Type:** `series int`
- **Description:** The number of analysts who gave the current symbol a "Strong Sell" rating.

### syminfo.recommendations_total

- **Type:** `series int`
- **Description:** The total number of recommendations for the current symbol.

### syminfo.root

- **Type:** `simple string`
- **Description:** Root for derivatives like futures contract. For other symbols returns the same value as syminfo.ticker.

### syminfo.sector

- **Type:** `simple string`
- **Description:** Returns the sector of the symbol, or na if the symbol has no sector. Example: "Electronic Technology", "Technology services", "Energy Minerals", "Consumer Durables", etc. These are the same values one can see in the chart's "Symbol info" window.

### syminfo.session

- **Type:** `simple string`
- **Description:** Session type of the chart main series. Possible values are session.regular, session.extended.

### syminfo.shareholders

- **Type:** `simple int`
- **Description:** The number of shareholders the company has.

### syminfo.shares_outstanding_float

- **Type:** `simple float`
- **Description:** The total number of shares outstanding a company has available, excluding any of its restricted shares.

### syminfo.shares_outstanding_total

- **Type:** `simple int`
- **Description:** The total number of shares outstanding a company has available, including restricted shares held by insiders, major shareholders, and employees.

### syminfo.target_price_average

- **Type:** `series float`
- **Description:** The average of the last yearly price targets for the symbol predicted by analysts.

### syminfo.target_price_date

- **Type:** `series int`
- **Description:** The starting date of the last price target prediction for the current symbol.

### syminfo.target_price_estimates

- **Type:** `series float`
- **Description:** The latest total number of price target predictions for the current symbol.

### syminfo.target_price_high

- **Type:** `series float`
- **Description:** The last highest yearly price target for the symbol predicted by analysts.

### syminfo.target_price_low

- **Type:** `series float`
- **Description:** The last lowest yearly price target for the symbol predicted by analysts.

### syminfo.target_price_median

- **Type:** `series float`
- **Description:** The median of the last yearly price targets for the symbol predicted by analysts.

### syminfo.ticker

- **Type:** `simple string`
- **Description:** Symbol name without exchange prefix, e.g. 'MSFT'.

### syminfo.tickerid

- **Type:** `simple string`
- **Description:** A ticker identifier representing the chart's symbol or a requested symbol, depending on how the script uses it. The variable's value represents a requested dataset's ticker ID when used in the expression argument of a request.*() function call. Otherwise, it represents the chart's ticker ID. The value contains an exchange prefix and a symbol name, separated by a colon (e.g., "NASDAQ:AAPL"). It can also include information about data modifications such as dividend adjustment, non-standard chart type, currency conversion, etc.

### syminfo.timezone

- **Type:** `simple string`
- **Description:** Timezone of the exchange of the chart main series. Possible values see in timestamp.

### syminfo.type

- **Type:** `simple string`
- **Description:** The type of market the symbol belongs to. The values are "stock", "fund", "dr", "right", "bond", "warrant", "structured", "index", "forex", "futures", "spread", "economic", "fundamental", "crypto", "spot", "swap", "option", "commodity".

### syminfo.volumetype

- **Type:** `simple string`
- **Description:** Volume type of the current symbol. Possible values are: "base" for base currency, "quote" for quote currency, "tick" for the number of transactions, and "n/a" when there is no volume or its type is not specified.

### ta.accdist

- **Type:** `series float`
- **Description:** Accumulation/distribution index.

### ta.iii

- **Type:** `series float`
- **Description:** Intraday Intensity Index.

### ta.nvi

- **Type:** `series float`
- **Description:** Negative Volume Index.

### ta.obv

- **Type:** `series float`
- **Description:** On Balance Volume.

### ta.pvi

- **Type:** `series float`
- **Description:** Positive Volume Index.

### ta.pvt

- **Type:** `series float`
- **Description:** Price-Volume Trend.

### ta.tr

- **Type:** `series float`
- **Description:** True range, equivalent to ta.tr(handle_na = false). It is calculated as math.max(high - low, math.abs(high - close[1]), math.abs(low - close[1])).

### ta.vwap

- **Type:** `series float`
- **Description:** Volume Weighted Average Price. It uses hlc3 as its source series.

### ta.wad

- **Type:** `series float`
- **Description:** Williams Accumulation/Distribution.

### ta.wvad

- **Type:** `series float`
- **Description:** Williams Variable Accumulation/Distribution.

### table.all

- **Type:** `array`
- **Description:** Returns an array filled with all the current tables drawn by the script.

### time

- **Type:** `series int`
- **Description:** Current bar time in UNIX format. It is the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970.

### time_close

- **Type:** `series int`
- **Description:** The time of the current bar's close in UNIX format. It represents the number of milliseconds elapsed since 00:00:00 UTC, 1 January 1970. On tick charts and price-based charts such as Renko, line break, Kagi, point & figure, and range, this variable's series holds an na timestamp for the latest realtime bar (because the future closing time is unpredictable), but valid timestamps for all previous bars.

### time_tradingday

- **Type:** `series int`
- **Description:** The beginning time of the trading day the current bar belongs to, in UNIX format (the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970).

### timeframe.isdaily

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a daily resolution, false otherwise.

### timeframe.isdwm

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a daily or weekly or monthly resolution, false otherwise.

### timeframe.isintraday

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is an intraday (minutes or seconds) resolution, false otherwise.

### timeframe.isminutes

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a minutes resolution, false otherwise.

### timeframe.ismonthly

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a monthly resolution, false otherwise.

### timeframe.isseconds

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a seconds resolution, false otherwise.

### timeframe.isticks

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a ticks resolution, false otherwise.

### timeframe.isweekly

- **Type:** `simple bool`
- **Description:** Returns true if current resolution is a weekly resolution, false otherwise.

### timeframe.main_period

- **Type:** `simple string`
- **Description:** A string representation of the script's main timeframe. If the script is an indicator that specifies a timeframe value in its declaration statement, this variable holds that value. Otherwise, its value represents the chart's timeframe. Unlike timeframe.period, this variable's value does not change when used in the expression argument of a request.*() function call.

### timeframe.multiplier

- **Type:** `simple int`
- **Description:** Multiplier of resolution, e.g. '60' - 60, 'D' - 1, '5D' - 5, '12M' - 12.

### timeframe.period

- **Type:** `simple string`
- **Description:** A string representation of the script's main timeframe or a requested timeframe, depending on how the script uses it. The variable's value represents the timeframe of a requested dataset when used in the expression argument of a request.*() function call. Otherwise, its value represents the script's main timeframe (timeframe.main_period), which equals either the timeframe argument of the indicator declaration statement or the chart's timeframe.

### timenow

- **Type:** `series int`
- **Description:** Current time in UNIX format. It is the number of milliseconds that have elapsed since 00:00:00 UTC, 1 January 1970.

### volume

- **Type:** `series float`
- **Description:** Current bar volume.

### weekofyear

- **Type:** `series int`
- **Description:** Week number of current bar time in exchange timezone.

### year

- **Type:** `series int`
- **Description:** Current bar year in exchange timezone.

## Constants

### adjustment.dividends

- **Type:** `const string`
- **Description:** Constant for dividends adjustment type (dividends adjustment is applied).

### adjustment.none

- **Type:** `const string`
- **Description:** Constant for none adjustment type (no adjustment is applied).

### adjustment.splits

- **Type:** `const string`
- **Description:** Constant for splits adjustment type (splits adjustment is applied).

### alert.freq_all

- **Type:** `const string`
- **Description:** A named constant for use with the freq parameter of the alert() function.

### alert.freq_once_per_bar

- **Type:** `const string`
- **Description:** A named constant for use with the freq parameter of the alert() function.

### alert.freq_once_per_bar_close

- **Type:** `const string`
- **Description:** A named constant for use with the freq parameter of the alert() function.

### backadjustment.inherit

- **Type:** `const backadjustment`
- **Description:** A constant to specify the value of the backadjustment parameter in ticker.new and ticker.modify functions.

### backadjustment.off

- **Type:** `const backadjustment`
- **Description:** A constant to specify the value of the backadjustment parameter in ticker.new and ticker.modify functions.

### backadjustment.on

- **Type:** `const backadjustment`
- **Description:** A constant to specify the value of the backadjustment parameter in ticker.new and ticker.modify functions.

### barmerge.gaps_off

- **Type:** `const barmerge_gaps`
- **Description:** Merge strategy for requested data. Data is merged continuously without gaps, all the gaps are filled with the previous nearest existing value.

### barmerge.gaps_on

- **Type:** `const barmerge_gaps`
- **Description:** Merge strategy for requested data. Data is merged with possible gaps (na values).

### barmerge.lookahead_off

- **Type:** `const barmerge_lookahead`
- **Description:** Merge strategy for the requested data position. Requested barset is merged with current barset in the order of sorting bars by their close time. This merge strategy disables effect of getting data from "future" on calculation on history.

### barmerge.lookahead_on

- **Type:** `const barmerge_lookahead`
- **Description:** Merge strategy for the requested data position. Requested barset is merged with current barset in the order of sorting bars by their opening time. This merge strategy can lead to undesirable effect of getting data from "future" on calculation on history. This is unacceptable in backtesting strategies, but can be useful in indicators.

### color.aqua

- **Type:** `const color`
- **Description:** Is a named constant for #00BCD4 color.

### color.black

- **Type:** `const color`
- **Description:** Is a named constant for #363A45 color.

### color.blue

- **Type:** `const color`
- **Description:** Is a named constant for #2962ff color.

### color.fuchsia

- **Type:** `const color`
- **Description:** Is a named constant for #E040FB color.

### color.gray

- **Type:** `const color`
- **Description:** Is a named constant for #787B86 color.

### color.green

- **Type:** `const color`
- **Description:** Is a named constant for #4CAF50 color.

### color.lime

- **Type:** `const color`
- **Description:** Is a named constant for #00E676 color.

### color.maroon

- **Type:** `const color`
- **Description:** Is a named constant for #880E4F color.

### color.navy

- **Type:** `const color`
- **Description:** Is a named constant for #311B92 color.

### color.olive

- **Type:** `const color`
- **Description:** Is a named constant for #808000 color.

### color.orange

- **Type:** `const color`
- **Description:** Is a named constant for #FF9800 color.

### color.purple

- **Type:** `const color`
- **Description:** Is a named constant for #9C27B0 color.

### color.red

- **Type:** `const color`
- **Description:** Is a named constant for #F23645 color.

### color.silver

- **Type:** `const color`
- **Description:** Is a named constant for #B2B5BE color.

### color.teal

- **Type:** `const color`
- **Description:** Is a named constant for #089981 color.

### color.white

- **Type:** `const color`
- **Description:** Is a named constant for #FFFFFF color.

### color.yellow

- **Type:** `const color`
- **Description:** Is a named constant for #FDD835 color.

### currency.AUD

- **Type:** `const string`
- **Description:** Australian dollar.

### currency.BTC

- **Type:** `const string`
- **Description:** Bitcoin.

### currency.CAD

- **Type:** `const string`
- **Description:** Canadian dollar.

### currency.CHF

- **Type:** `const string`
- **Description:** Swiss franc.

### currency.EGP

- **Type:** `const string`
- **Description:** Egyptian pound.

### currency.ETH

- **Type:** `const string`
- **Description:** Ethereum.

### currency.EUR

- **Type:** `const string`
- **Description:** Euro.

### currency.GBP

- **Type:** `const string`
- **Description:** Pound sterling.

### currency.HKD

- **Type:** `const string`
- **Description:** Hong Kong dollar.

### currency.INR

- **Type:** `const string`
- **Description:** Indian rupee.

### currency.JPY

- **Type:** `const string`
- **Description:** Japanese yen.

### currency.KRW

- **Type:** `const string`
- **Description:** South Korean won.

### currency.MYR

- **Type:** `const string`
- **Description:** Malaysian ringgit.

### currency.NOK

- **Type:** `const string`
- **Description:** Norwegian krone.

### currency.NONE

- **Type:** `const string`
- **Description:** Unspecified currency.

### currency.NZD

- **Type:** `const string`
- **Description:** New Zealand dollar.

### currency.PKR

- **Type:** `const string`
- **Description:** Pakistani rupee.

### currency.PLN

- **Type:** `const string`
- **Description:** Polish zloty.

### currency.RUB

- **Type:** `const string`
- **Description:** Russian ruble.

### currency.SEK

- **Type:** `const string`
- **Description:** Swedish krona.

### currency.SGD

- **Type:** `const string`
- **Description:** Singapore dollar.

### currency.TRY

- **Type:** `const string`
- **Description:** Turkish lira.

### currency.USD

- **Type:** `const string`
- **Description:** United States dollar.

### currency.USDT

- **Type:** `const string`
- **Description:** Tether.

### currency.ZAR

- **Type:** `const string`
- **Description:** South African rand.

### dayofweek.friday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.monday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.saturday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.sunday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.thursday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.tuesday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### dayofweek.wednesday

- **Type:** `const int`
- **Description:** Is a named constant for return value of dayofweek function and value of dayofweek variable.

### display.all

- **Type:** `const plot_simple_display`
- **Description:** A named constant for use with the display parameter of plot*() and input*() functions. Displays plotted or input values in all possible locations.

### display.data_window

- **Type:** `const plot_display`
- **Description:** A named constant for use with the display parameter of plot*() and input*() functions. Displays plotted or input values in the Data Window, a menu accessible from the chart's right sidebar.

### display.none

- **Type:** `const plot_simple_display`
- **Description:** A named constant for use with the display parameter of plot*() and input*() functions. plot*() functions using this will not display their plotted values anywhere. However, alert template messages and fill functions can still use the values, and they will appear in exported chart data. input*() functions using this constant will only display their values within the script's settings.

### display.pane

- **Type:** `const plot_display`
- **Description:** A named constant for use with the display parameter of plot*() functions. Displays plotted values in the chart pane used by the script.

### display.price_scale

- **Type:** `const plot_display`
- **Description:** A named constant for use with the display parameter of plot*() functions. Displays the plot’s label and value on the price scale if the chart's settings allow it.

### display.status_line

- **Type:** `const plot_display`
- **Description:** A named constant for use with the display parameter of plot*() and input*() functions. Displays plotted or input values in the status line next to the script's name on the chart if the chart's settings allow it.

### dividends.gross

- **Type:** `const string`
- **Description:** A named constant for the request.dividends function. Is used to request the dividends return on a stock before deductions.

### dividends.net

- **Type:** `const string`
- **Description:** A named constant for the request.dividends function. Is used to request the dividends return on a stock after deductions.

### earnings.actual

- **Type:** `const string`
- **Description:** A named constant for the request.earnings function. Is used to request the earnings value as it was reported.

### earnings.estimate

- **Type:** `const string`
- **Description:** A named constant for the request.earnings function. Is used to request the estimated earnings value.

### earnings.standardized

- **Type:** `const string`
- **Description:** A named constant for the request.earnings function. Is used to request the standardized earnings value.

### extend.both

- **Type:** `const string`
- **Description:** A named constant for line.new and line.set_extend functions.

### extend.left

- **Type:** `const string`
- **Description:** A named constant for line.new and line.set_extend functions.

### extend.none

- **Type:** `const string`
- **Description:** A named constant for line.new and line.set_extend functions.

### extend.right

- **Type:** `const string`
- **Description:** A named constant for line.new and line.set_extend functions.

### false

- **Type:** `Literal`
- **Description:** Literal representing a bool value, and result of a comparison operation.

### font.family_default

- **Type:** `const string`
- **Description:** Default text font for box.new, box.set_text_font_family, label.new, label.set_text_font_family, table.cell and table.cell_set_text_font_family functions.

### font.family_monospace

- **Type:** `const string`
- **Description:** Monospace text font for box.new, box.set_text_font_family, label.new, label.set_text_font_family, table.cell and table.cell_set_text_font_family functions.

### format.inherit

- **Type:** `const string`
- **Description:** Is a named constant for selecting the formatting of the script output values from the parent series in the indicator function.

### format.mintick

- **Type:** `const string`
- **Description:** Is a named constant to use with the str.tostring function. Passing a number to str.tostring with this argument rounds the number to the nearest value that can be divided by syminfo.mintick, without the remainder, with ties rounding up, and returns the string version of said value with trailing zeros.

### format.percent

- **Type:** `const string`
- **Description:** Is a named constant for selecting the formatting of the script output values as a percentage in the indicator function. It adds a percent sign after values.

### format.price

- **Type:** `const string`
- **Description:** Is a named constant for selecting the formatting of the script output values as prices in the indicator function.

### format.volume

- **Type:** `const string`
- **Description:** Is a named constant for selecting the formatting of the script output values as volume in the indicator function, e.g. '5183' will be formatted as '5.183K'.

### hline.style_dashed

- **Type:** `const hline_style`
- **Description:** Is a named constant for dashed linestyle of hline function.

### hline.style_dotted

- **Type:** `const hline_style`
- **Description:** Is a named constant for dotted linestyle of hline function.

### hline.style_solid

- **Type:** `const hline_style`
- **Description:** Is a named constant for solid linestyle of hline function.

### label.style_arrowdown

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_arrowup

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_circle

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_cross

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_diamond

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_flag

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_center

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_down

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_left

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_lower_left

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_lower_right

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_right

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_up

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_upper_left

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_label_upper_right

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_none

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_square

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_text_outline

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_triangledown

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_triangleup

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### label.style_xcross

- **Type:** `const string`
- **Description:** Label style for label.new and label.set_style functions.

### line.style_arrow_both

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions. Solid line with arrows on both points.

### line.style_arrow_left

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions. Solid line with arrow on the first point.

### line.style_arrow_right

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions. Solid line with arrow on the second point.

### line.style_dashed

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions.

### line.style_dotted

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions.

### line.style_solid

- **Type:** `const string`
- **Description:** Line style for line.new and line.set_style functions.

### location.abovebar

- **Type:** `const string`
- **Description:** Location value for plotshape, plotchar functions. Shape is plotted above main series bars.

### location.absolute

- **Type:** `const string`
- **Description:** Location value for plotshape, plotchar functions. Shape is plotted on chart using indicator value as a price coordinate.

### location.belowbar

- **Type:** `const string`
- **Description:** Location value for plotshape, plotchar functions. Shape is plotted below main series bars.

### location.bottom

- **Type:** `const string`
- **Description:** Location value for plotshape, plotchar functions. Shape is plotted near the bottom chart border.

### location.top

- **Type:** `const string`
- **Description:** Location value for plotshape, plotchar functions. Shape is plotted near the top chart border.

### math.e

- **Type:** `const float`
- **Description:** Is a named constant for Euler's number. It is equal to 2.7182818284590452.

### math.phi

- **Type:** `const float`
- **Description:** Is a named constant for the golden ratio. It is equal to 1.6180339887498948.

### math.pi

- **Type:** `const float`
- **Description:** Is a named constant for Archimedes' constant. It is equal to 3.1415926535897932.

### math.rphi

- **Type:** `const float`
- **Description:** Is a named constant for the golden ratio conjugate. It is equal to 0.6180339887498948.

### order.ascending

- **Type:** `const sort_order`
- **Description:** Determines the sort order of the array from the smallest to the largest value.

### order.descending

- **Type:** `const sort_order`
- **Description:** Determines the sort order of the array from the largest to the smallest value.

### plot.style_area

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Area' style, to be used as an argument for the style parameter in the plot function.

### plot.style_areabr

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Area With Breaks' style, to be used as an argument for the style parameter in the plot function. Similar to plot.style_area, except the gaps in the data are not filled.

### plot.style_circles

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Circles' style, to be used as an argument for the style parameter in the plot function.

### plot.style_columns

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Columns' style, to be used as an argument for the style parameter in the plot function.

### plot.style_cross

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Cross' style, to be used as an argument for the style parameter in the plot function.

### plot.style_histogram

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Histogram' style, to be used as an argument for the style parameter in the plot function.

### plot.style_line

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Line' style, to be used as an argument for the style parameter in the plot function.

### plot.style_linebr

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Line With Breaks' style, to be used as an argument for the style parameter in the plot function. Similar to plot.style_line, except the gaps in the data are not filled.

### plot.style_stepline

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Step Line' style, to be used as an argument for the style parameter in the plot function.

### plot.style_stepline_diamond

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Step Line With Diamonds' style, to be used as an argument for the style parameter in the plot function. Similar to plot.style_stepline, except the data changes are also marked with the Diamond shapes.

### plot.style_steplinebr

- **Type:** `const plot_style`
- **Description:** A named constant for the 'Step line with Breaks' style, to be used as an argument for the style parameter in the plot function.

### position.bottom_center

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.bottom_left

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.bottom_right

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.middle_center

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.middle_left

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.middle_right

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.top_center

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.top_left

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### position.top_right

- **Type:** `const string`
- **Description:** Table position is used in table.new, table.cell functions.

### scale.left

- **Type:** `const scale_type`
- **Description:** Scale value for indicator function. Indicator is added to the left price scale.

### scale.none

- **Type:** `const scale_type`
- **Description:** Scale value for indicator function. Indicator is added in 'No Scale' mode. Can be used only with 'overlay=true'.

### scale.right

- **Type:** `const scale_type`
- **Description:** Scale value for indicator function. Indicator is added to the right price scale.

### session.extended

- **Type:** `const string`
- **Description:** Constant for extended session type (with extended hours data).

### session.regular

- **Type:** `const string`
- **Description:** Constant for regular session type (no extended hours data).

### settlement_as_close.inherit

- **Type:** `const settlement`
- **Description:** A constant to specify the value of the settlement_as_close parameter in ticker.new and ticker.modify functions.

### settlement_as_close.off

- **Type:** `const settlement`
- **Description:** A constant to specify the value of the settlement_as_close parameter in ticker.new and ticker.modify functions.

### settlement_as_close.on

- **Type:** `const settlement`
- **Description:** A constant to specify the value of the settlement_as_close parameter in ticker.new and ticker.modify functions.

### shape.arrowdown

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.arrowup

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.circle

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.cross

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.diamond

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.flag

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.labeldown

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.labelup

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.square

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.triangledown

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.triangleup

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### shape.xcross

- **Type:** `const string`
- **Description:** Shape style for plotshape function.

### size.auto

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape automatically adapts to the size of the bars.

### size.huge

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape constantly huge.

### size.large

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape constantly large.

### size.normal

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape constantly normal.

### size.small

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape constantly small.

### size.tiny

- **Type:** `const string`
- **Description:** Size value for plotshape, plotchar functions. The size of the shape constantly tiny.

### splits.denominator

- **Type:** `const string`
- **Description:** A named constant for the request.splits function. Is used to request the denominator (the number below the line in a fraction) of a splits.

### splits.numerator

- **Type:** `const string`
- **Description:** A named constant for the request.splits function. Is used to request the numerator (the number above the line in a fraction) of a splits.

### strategy.cash

- **Type:** `const string`
- **Description:** This is one of the arguments that can be supplied to the default_qty_type parameter in the strategy declaration statement. It is only relevant when no value is used for the ‘qty’ parameter in strategy.entry or strategy.order function calls. It specifies that an amount of cash in the strategy.account_currency will be used to enter trades.
