from training.main import main
from utils.enums import KPIType


def test_main(mocker):
    """Test the main function of the training module."""

    # Mock the functions used in the main function
    input_data_mock = mocker.MagicMock()
    load = mocker.patch("training.main.load", return_value=input_data_mock)

    model_spec_mock = mocker.MagicMock()
    prepare = mocker.patch("training.main.prepare", return_value=model_spec_mock)

    meridian_model_mock = mocker.MagicMock()
    train = mocker.patch("training.main.train", return_value=meridian_model_mock)

    save = mocker.patch("training.main.save", return_value=None)

    # Example parameters for the main function
    params = {
        "csv_path": "data/input.csv",
        "kpi_type": KPIType.REVENUE,
        "time": "date",
        "kpi": "revenue",
        "controls": ["ad_spend", "seasonality"],
        "geo": "region",
        "population": "population_size",
        "roi_mu": 0.1,
        "roi_sigma": 0.05,
        "max_lag": 3,
        "n_draws": 1000,
        "n_chains": 4,
        "n_adapt": 500,
        "n_burnin": 2000,
        "n_keep": 1000,
        "file_path": "models/trained_model.pkl",
    }

    # Call the main function with the example parameters
    main(**params)

    # Asserts
    load.assert_called_once_with(
        csv_path=params["csv_path"],
        kpi_type=params["kpi_type"],
        time=params["time"],
        kpi=params["kpi"],
        controls=params["controls"],
        geo=params["geo"],
        population=params["population"],
        revenue_per_kpi=None,
        media=None,
        media_spend=None,
        organic_media=None,
        non_media_treatments=None,
    )
    prepare.assert_called_once_with(
        roi_mu=params["roi_mu"],
        roi_sigma=params["roi_sigma"],
        max_lag=params["max_lag"],
    )

    train.assert_called_once_with(
        input_data=input_data_mock,
        model_spec=model_spec_mock,
        n_draws=params["n_draws"],
        n_chains=params["n_chains"],
        n_adapt=params["n_adapt"],
        n_burnin=params["n_burnin"],
        n_keep=params["n_keep"],
    )

    save.assert_called_once_with(
        meridian_model_mock,
        params["file_path"],
    )
