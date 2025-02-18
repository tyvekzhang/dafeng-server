from src.main.app.controller.sys_dict_data_controller import dict_data_router

router.include_router(dict_data_router, tags=["dict-data"], prefix="/dict-data")