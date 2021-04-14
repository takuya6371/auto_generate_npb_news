import api.util.npb_const as nc
import api.util.common_func as cf
import api.domain.news_sentense_game_detail.game_hightlight_info as hi
import api.domain.news_sentense_game_detail.game_hightlight_play_list as pl
import api.domain.news_sentense_game_detail.sentense as s

def run (game_data_df):
    hightlight_info = hi.extract_game_hightlight_info(
        game_data_df['visitor_score_board'],
        game_data_df['home_score_board'],
    )
    hightlight_inning_play_list = pl.extract_hightlight_inning_play_list(
        game_data_df['visitor_score_board'],
        game_data_df['home_score_board'],
        hightlight_info,
        game_data_df['playbyplay'],
    )
    sentense = s.extract_sentense(
        game_data_df['home_team'],
        game_data_df['visitor_team'],
        hightlight_info,
        hightlight_inning_play_list,
    )
    print(sentense)

    return sentense
