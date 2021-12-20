"""
Module for bot configuration functionality.

This module contains the `BotConfig` class that implements a conversational
sequence in order to configure the bot behavior.
"""
from typing import TYPE_CHECKING, Callable, List

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    ConversationHandler,
    Filters,
    MessageHandler
)

if TYPE_CHECKING:  # pragma: no cover
    from surveillance_bot.bot import Bot  # pylint: disable=cyclic-import


class BotConfig:
    """
    Class for bot configuration process implementation.

    This class contains all constants and static methods needed to implements
    a conversational sequence with the user in order to the bot behavior will
    be configured.

    It doesn't have any instance method so it doesn't need to be instantiated.
    """
    # Configuration variables
    TIMESTAMP = 'timestamp'
    OD_VIDEO_DURATION = 'od_video_duration'
    SRV_VIDEO_DURATION = 'srv_video_duration'
    SRV_AUDIO_DURATION = 'srv_audio_duration'
    SRV_PICTURE_INTERVAL = 'srv_picture_interval'
    SRV_MOTION_CONTOURS = 'srv_motion_contours'
    SRV_VIDEO_THRESHOLD = 'srv_video_threshold'
    SRV_AUDIO_THRESHOLD = 'srv_audio_threshold'

    # State definitions for top level conversation
    MAIN_MENU, GENERAL_CONFIG, SURVEILLANCE_CONFIG = map(chr, range(3))

    # State definitions for second level conversation
    (
        CHANGE_TIMESTAMP,
        CHANGE_OD_VIDEO_DURATION,
        CHANGE_SRV_VIDEO_DURATION,
        CHANGE_SRV_AUDIO_DURATION,
        CHANGE_SRV_PICTURE_INTERVAL,
        CHANGE_SRV_MOTION_CONTOURS,
        CHANGE_SRV_VIDEO_THRESHOLD,
        CHANGE_SRV_AUDIO_THRESHOLD
    ) = map(chr, range(3, 11))

    # State definitions for input conversation
    BOOLEAN_INPUT, INTEGER_INPUT, FLOAT_INPUT = map(chr, range(11, 14))

    # Shortcut for ConversationHandler.END
    END = ConversationHandler.END

    # Auxiliary constants
    CURRENT_VARIABLE, RETURN_HANDLER, ENABLE, DISABLE = map(chr, range(14, 18))

    @staticmethod
    def get_config_handler(bot: 'Bot') -> ConversationHandler:
        """
        Generates the conversation handler for whole configuration process.

        Args:
            bot: The parent `Bot` instance.

        Returns:
            The instantiated `ConversationHandler`.
        """
        main_handler = ConversationHandler(
            entry_points=[bot.command_handler('config', BotConfig._main_menu)],
            states={
                BotConfig.MAIN_MENU: [
                    CallbackQueryHandler(
                        BotConfig._general_config,
                        pattern='^' + str(BotConfig.GENERAL_CONFIG) + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._surveillance_config,
                        pattern='^' + str(BotConfig.SURVEILLANCE_CONFIG) + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._end,
                        pattern='^' + str(BotConfig.END) + '$'
                    )
                ],
                BotConfig.GENERAL_CONFIG: [
                    CallbackQueryHandler(
                        BotConfig._change_timestamp,
                        pattern='^'
                        + str(BotConfig.CHANGE_TIMESTAMP)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_od_video_duration,
                        pattern='^'
                        + str(BotConfig.CHANGE_OD_VIDEO_DURATION)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._main_menu,
                        pattern='^' + str(BotConfig.END) + '$'
                    )
                ],
                BotConfig.SURVEILLANCE_CONFIG: [
                    CallbackQueryHandler(
                        BotConfig._change_srv_video_duration,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_VIDEO_DURATION)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_srv_audio_duration,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_AUDIO_DURATION)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_srv_picture_interval,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_PICTURE_INTERVAL)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_motion_contours,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_MOTION_CONTOURS)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_srv_video_threshold,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_VIDEO_THRESHOLD)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._change_srv_audio_threshold,
                        pattern='^'
                        + str(BotConfig.CHANGE_SRV_AUDIO_THRESHOLD)
                        + '$'
                    ),
                    CallbackQueryHandler(
                        BotConfig._main_menu,
                        pattern='^' + str(BotConfig.END) + '$'
                    )
                ],
                BotConfig.BOOLEAN_INPUT: [
                    CallbackQueryHandler(
                        BotConfig._boolean_input,
                        pattern='^'
                        + str(BotConfig.ENABLE)
                        + '$|^'
                        + str(BotConfig.DISABLE)
                        + '$'
                    )
                ],
                BotConfig.INTEGER_INPUT: [
                    MessageHandler(
                        Filters.text,
                        BotConfig._integer_input
                    )
                ],
                BotConfig.FLOAT_INPUT: [
                    MessageHandler(
                        Filters.text,
                        BotConfig._float_input
                    )
                ]
            },
            fallbacks=[bot.command_handler('stop_config', BotConfig._end)],
        )

        return main_handler

    @staticmethod
    def ensure_defaults(context: CallbackContext) -> None:
        """
        Creates non-existent variables and populates with default values.

        Args:
            context: The context object for the update.
        """
        if BotConfig.TIMESTAMP not in context.bot_data:
            context.bot_data[BotConfig.TIMESTAMP] = True

        if BotConfig.OD_VIDEO_DURATION not in context.bot_data:
            context.bot_data[BotConfig.OD_VIDEO_DURATION] = 5

        if BotConfig.SRV_VIDEO_DURATION not in context.bot_data:
            context.bot_data[BotConfig.SRV_VIDEO_DURATION] = 30

        if BotConfig.SRV_AUDIO_DURATION not in context.bot_data:
            context.bot_data[BotConfig.SRV_AUDIO_DURATION] = 5

        if BotConfig.SRV_PICTURE_INTERVAL not in context.bot_data:
            context.bot_data[BotConfig.SRV_PICTURE_INTERVAL] = 5

        if BotConfig.SRV_MOTION_CONTOURS not in context.bot_data:
            context.bot_data[BotConfig.SRV_MOTION_CONTOURS] = True

        if BotConfig.SRV_VIDEO_THRESHOLD not in context.bot_data:
            context.bot_data[BotConfig.SRV_VIDEO_THRESHOLD] = 5

        if BotConfig.SRV_AUDIO_THRESHOLD not in context.bot_data:
            context.bot_data[BotConfig.SRV_AUDIO_THRESHOLD] = 0.1

    # Menus

    @staticmethod
    def _main_menu(update: Update, _: CallbackContext) -> str:
        """
        Creates the main menu and send it to the user.

        This menu links to the general configuration and to the surveillance
        mode configuration.

        Args:
            update: The update to be handled.

        Returns:
            The state MAIN_MENU.
        """
        text = "*Surveillance Telegram Bot Configuration*\n" \
               "\n" \
               "Here you can modify some bot behavior parameters|. \n" \
               "\n" \
               "While the mode is running it does not allow you any change " \
               "unless you restart it|.\n" \
               "\n" \
               "To abort type /stop|_config|.\n" \
               "\n" \
               "Select section:".replace('|', '\\')
        buttons = [
            [InlineKeyboardButton(
                text='General configuration',
                callback_data=str(BotConfig.GENERAL_CONFIG)
            )],
            [InlineKeyboardButton(
                text='Surveillance mode configuration',
                callback_data=str(BotConfig.SURVEILLANCE_CONFIG)
            )],
            [InlineKeyboardButton(
                text='Done',
                callback_data=str(BotConfig.END)
            )]
        ]

        BotConfig._render_menu(update, text, buttons)

        return BotConfig.MAIN_MENU

    @staticmethod
    def _general_config(update: Update, context: CallbackContext) -> str:
        """
        Creates the menu for general configuration and send it to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state GENERAL_CONFIG.
        """
        timestamp = context.bot_data[BotConfig.TIMESTAMP]
        video_duration = context.bot_data[BotConfig.OD_VIDEO_DURATION]

        timestamp_str = 'Enabled' if timestamp else 'Disabled'

        text = f"*General configuration*\n" \
               f"\n" \
               f"__Timestamp__:\n" \
               f" |- _Description_: Print a timestamp on every photo or" \
               f" video taken|.\n" \
               f" |- _Current value_: *{timestamp_str}*\n" \
               f"\n" \
               f"__On Demand video duration__:\n" \
               f" |- _Description_: Duration of the video taken with " \
               f"/get|_video command|.\n" \
               f" |- _Current value_: *{video_duration} seconds*" \
               f"".replace('|', '\\')
        buttons = [
            [InlineKeyboardButton(
                text='Timestamp',
                callback_data=str(BotConfig.CHANGE_TIMESTAMP)
            )],
            [InlineKeyboardButton(
                text='On Demand video duration',
                callback_data=str(BotConfig.CHANGE_OD_VIDEO_DURATION)
            )],
            [InlineKeyboardButton(
                text='Back',
                callback_data=str(BotConfig.END)
            )]
        ]

        BotConfig._render_menu(update, text, buttons)

        return BotConfig.GENERAL_CONFIG

    @staticmethod
    def _surveillance_config(update: Update, context: CallbackContext) -> str:
        """
        Creates the menu for the surveillance mode configuration and send it
        to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state SURVEILLANCE_CONFIG.
        """
        video_duration = context.bot_data[BotConfig.SRV_VIDEO_DURATION]
        audio_duration = context.bot_data[BotConfig.SRV_AUDIO_DURATION]
        picture_interval = context.bot_data[BotConfig.SRV_PICTURE_INTERVAL]
        motion_contours = context.bot_data[BotConfig.SRV_MOTION_CONTOURS]
        video_threshold = context.bot_data[BotConfig.SRV_VIDEO_THRESHOLD]
        audio_threshold = context.bot_data[BotConfig.SRV_AUDIO_THRESHOLD]

        motion_contours_str = 'Enabled' if motion_contours else 'Disabled'

        text = f"*Surveillance Mode configuration*\n" \
               f"\n" \
               f"__Video duration__:\n" \
               f" |- _Description_: Duration of the video taken when motion " \
               f"or sound is detected|.\n" \
               f" |- _Current value_: *{video_duration} seconds*\n" \
               f"\n" \
               f"__Audio duration__:\n" \
               f" |- _Description_: Duration of the audio recorded when motion " \
               f"or sound is detected|.\n" \
               f" |- _Current value_: *{audio_duration} seconds*\n" \
               f"\n" \
               f"__Picture Interval__:\n" \
               f" |- _Description_: Interval between photos taken after " \
               f"motion is detected|.\n" \
               f" |- _Current value_: *{picture_interval} seconds*\n" \
               f"\n" \
               f"__Draw motion contours__:\n" \
               f" |- _Description_: Draws a rectangle around the objects in " \
               f"motion|.\n" \
               f" |- _Current value_: *{motion_contours_str}*" \
               f"\n" \
               f"__Video threshold__:\n" \
               f" |- _Description_: Sensitivity of motion detection|.\n" \
               f" |- _Current value_: *{video_threshold}*\n" \
               f"\n" \
               f"__Audio threshold__:\n" \
               f" |- _Description_: Sensitivity of sound detection|.\n" \
               f" |- _Current value_: *{str(audio_threshold).replace('.', '|.')}*\n" \
               f"".replace('|', '\\')
        buttons = [
            [InlineKeyboardButton(
                text='Video duration',
                callback_data=str(BotConfig.CHANGE_SRV_VIDEO_DURATION)
            )],
            [InlineKeyboardButton(
                text='Audio duration',
                callback_data=str(BotConfig.CHANGE_SRV_AUDIO_DURATION)
            )],
            [InlineKeyboardButton(
                text='Picture Interval',
                callback_data=str(BotConfig.CHANGE_SRV_PICTURE_INTERVAL)
            )],
            [InlineKeyboardButton(
                text='Draw motion contours',
                callback_data=str(BotConfig.CHANGE_SRV_MOTION_CONTOURS)
            )],
            [InlineKeyboardButton(
                text='Video threshold',
                callback_data=str(BotConfig.CHANGE_SRV_VIDEO_THRESHOLD)
            )],
            [InlineKeyboardButton(
                text='Audio threshold',
                callback_data=str(BotConfig.CHANGE_SRV_AUDIO_THRESHOLD)
            )],
            [InlineKeyboardButton(
                text='Back',
                callback_data=str(BotConfig.END)
            )]
        ]

        BotConfig._render_menu(update, text, buttons)

        return BotConfig.SURVEILLANCE_CONFIG

    @staticmethod
    def _render_menu(
            update: Update,
            text: str,
            buttons: List[List[InlineKeyboardButton]]
    ) -> None:
        """
        Builds the inline keyboard for the menu and sends all to the user.

        Args:
            update: The update to be handled.
            text: Text for the menu caption.
            buttons: Array of button rows,
                each represented by an Array of InlineKeyboardButton objects.
        """
        keyboard = InlineKeyboardMarkup(buttons)

        if update.message:
            update.message.reply_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        else:
            update.callback_query.answer()
            update.callback_query.edit_message_text(
                text=text,
                reply_markup=keyboard,
                parse_mode=ParseMode.MARKDOWN_V2
            )

    # General configuration options.

    @staticmethod
    def _change_timestamp(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the TIMESTAMP configuration to
        the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state BOOLEAN_INPUT through `_boolean_question` method.
        """
        timestamp = context.bot_data[BotConfig.TIMESTAMP]

        timestamp_str = 'Enabled' if timestamp else 'Disabled'

        text = f'*Timestamp*\n' \
               f'\n' \
               f'Current state: *{timestamp_str}*\n' \
               f'\n' \
               f'Select state for time stamping:'

        return BotConfig._boolean_question(
            update,
            context,
            text,
            BotConfig.TIMESTAMP,
            BotConfig._general_config
        )

    @staticmethod
    def _change_od_video_duration(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the OD_VIDEO_DURATION
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state INTEGER_INPUT through `_integer_question` method.
        """
        video_duration = context.bot_data[BotConfig.OD_VIDEO_DURATION]

        text = f'*On Demand video duration*\n' \
               f'\n' \
               f'Current value: *{video_duration}*\n' \
               f'\n' \
               f'Type value for video duration:'

        return BotConfig._integer_question(
            update,
            context,
            text,
            BotConfig.OD_VIDEO_DURATION,
            BotConfig._general_config
        )

    # Surveillance mode configuration options.

    @staticmethod
    def _change_srv_video_duration(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_VIDEO_DURATION
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state INTEGER_INPUT through `_integer_question` method.
        """
        video_duration = context.bot_data[BotConfig.SRV_VIDEO_DURATION]

        text = f'*Surveillance video duration*\n' \
               f'\n' \
               f'Current value: *{video_duration}*\n' \
               f'\n' \
               f'Type value for video duration:'

        return BotConfig._integer_question(
            update,
            context,
            text,
            BotConfig.SRV_VIDEO_DURATION,
            BotConfig._surveillance_config
        )

    @staticmethod
    def _change_srv_audio_duration(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_AUDIO_DURATION
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state INTEGER_INPUT through `_integer_question` method.
        """
        audio_duration = context.bot_data[BotConfig.SRV_AUDIO_DURATION]

        text = f'*Surveillance audio duration*\n' \
               f'\n' \
               f'Current value: *{audio_duration}*\n' \
               f'\n' \
               f'Type value for video duration:'

        return BotConfig._integer_question(
            update,
            context,
            text,
            BotConfig.SRV_AUDIO_DURATION,
            BotConfig._surveillance_config
        )

    @staticmethod
    def _change_srv_picture_interval(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_PICTURE_INTERVAL
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state INTEGER_INPUT through `_integer_question` method.
        """
        picture_interval = context.bot_data[BotConfig.SRV_PICTURE_INTERVAL]

        text = f'*Surveillance picture interval*\n' \
               f'\n' \
               f'Current value: *{picture_interval}*\n' \
               f'\n' \
               f'Type value for picture interval:'

        return BotConfig._integer_question(
            update,
            context,
            text,
            BotConfig.SRV_PICTURE_INTERVAL,
            BotConfig._surveillance_config
        )

    @staticmethod
    def _change_motion_contours(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_MOTION_CONTOURS
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state BOOLEAN_INPUT through `_boolean_question` method.
        """
        motion_contours = context.bot_data[BotConfig.SRV_MOTION_CONTOURS]

        motion_contours_str = 'Enabled' if motion_contours else 'Disabled'

        text = f'*Motion contours*\n' \
               f'\n' \
               f'Current state: *{motion_contours_str}*\n' \
               f'\n' \
               f'Select state for motion contours:'

        return BotConfig._boolean_question(
            update,
            context,
            text,
            BotConfig.SRV_MOTION_CONTOURS,
            BotConfig._surveillance_config
        )

    @staticmethod
    def _change_srv_video_threshold(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_VIDEO_THRESHOLD
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state INTEGER_INPUT through `_integer_question` method.
        """
        video_threshold = context.bot_data[BotConfig.SRV_VIDEO_THRESHOLD]

        text = f'*Video threshold*\n' \
               f'\n' \
               f'Current value: *{video_threshold}*\n' \
               f'\n' \
               f'Type value for video threshold \\(e\\.g\\., 5\\):'

        return BotConfig._integer_question(
            update,
            context,
            text,
            BotConfig.SRV_VIDEO_THRESHOLD,
            BotConfig._surveillance_config
        )

    @staticmethod
    def _change_srv_audio_threshold(
            update: Update,
            context: CallbackContext
    ) -> str:
        """
        Prepares all required data to request the SRV_AUDIO_THRESHOLD
        configuration to the user.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state FLOAT_INPUT through `_float_question` method.
        """
        audio_threshold = context.bot_data[BotConfig.SRV_AUDIO_THRESHOLD]

        text = '*Audio threshold*\n' \
               '\n' \
               'Current value: *' + str(audio_threshold).replace(".", "\\.") + '*\n' \
               '\n' \
               'Type value for audio threshold \\(e\\.g\\., 0\\.1\\):'

        return BotConfig._float_question(
            update,
            context,
            text,
            BotConfig.SRV_AUDIO_THRESHOLD,
            BotConfig._surveillance_config
        )

    # Questions helpers.

    @staticmethod
    def _boolean_question(
            update: Update,
            context: CallbackContext,
            text: str,
            current_variable: str,
            return_handler: Callable[[Update, CallbackContext], str]
    ) -> str:
        """
        Builds a boolean question to send it to the user using received data.

        Args:
            update: The update to be handled.
            context: The context object for the update.
            text: Message to be shown to the users.
            current_variable: Variable to be set.
            return_handler: Handler to be called with the user response.

        Returns:
            The state BOOLEAN_INPUT.
        """
        context.user_data[BotConfig.CURRENT_VARIABLE] = current_variable
        context.user_data[BotConfig.RETURN_HANDLER] = return_handler

        buttons = [[
            InlineKeyboardButton(
                text='Enable',
                callback_data=str(BotConfig.ENABLE)
            ),
            InlineKeyboardButton(
                text='Disable',
                callback_data=str(BotConfig.DISABLE)
            ),
        ]]
        keyboard = InlineKeyboardMarkup(buttons)

        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return BotConfig.BOOLEAN_INPUT

    @staticmethod
    def _integer_question(
            update: Update,
            context: CallbackContext,
            text: str,
            current_variable: str,
            return_handler: Callable[[Update, CallbackContext], str]
    ) -> str:
        """
        Builds a integer question to send it to the user using received data.

        Args:
            update: The update to be handled.
            context: The context object for the update.
            text: Message to be shown to the users.
            current_variable: Variable to be set.
            return_handler: Handler to be called with the user response.

        Returns:
            The state INTEGER_INPUT.
        """
        context.user_data[BotConfig.CURRENT_VARIABLE] = current_variable
        context.user_data[BotConfig.RETURN_HANDLER] = return_handler

        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return BotConfig.INTEGER_INPUT

    @staticmethod
    def _float_question(
            update: Update,
            context: CallbackContext,
            text: str,
            current_variable: str,
            return_handler: Callable[[Update, CallbackContext], str]
    ) -> str:
        """
        Builds a floating point question to send it to the user using received data.

        Args:
            update: The update to be handled.
            context: The context object for the update.
            text: Message to be shown to the users.
            current_variable: Variable to be set.
            return_handler: Handler to be called with the user response.

        Returns:
            The state FLOAT_INPUT.
        """
        context.user_data[BotConfig.CURRENT_VARIABLE] = current_variable
        context.user_data[BotConfig.RETURN_HANDLER] = return_handler

        update.callback_query.answer()
        update.callback_query.edit_message_text(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2
        )

        return BotConfig.FLOAT_INPUT

    # Input handlers.

    @staticmethod
    def _boolean_input(update: Update, context: CallbackContext) -> str:
        """
        Receive a boolean input from the user and saves the value into
        corresponding variable.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The execution of the previously stored handler.
        """
        context.bot_data[
            context.user_data[BotConfig.CURRENT_VARIABLE]
        ] = update.callback_query.data == BotConfig.ENABLE

        return context.user_data[BotConfig.RETURN_HANDLER](update, context)

    @staticmethod
    def _integer_input(update: Update, context: CallbackContext) -> str:
        """
        Receive a integer input from the user, validates it, and saves the
        value into corresponding variable.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The execution of the previously stored handler or the state
                INTEGER_INPUT in case of validation error.
        """
        try:
            value = int(update.message.text)
            assert value >= 0
            assert value <= 255
        except (ValueError, AssertionError):
            update.message.reply_text(
                text='Invalid value, insert an integer number between 0 and 255'
            )
            return BotConfig.INTEGER_INPUT

        context.bot_data[
            context.user_data[BotConfig.CURRENT_VARIABLE]
        ] = value

        return context.user_data[BotConfig.RETURN_HANDLER](update, context)

    @staticmethod
    def _float_input(update: Update, context: CallbackContext) -> str:
        """
        Receive a floatng point input from the user, validates it, and saves the
        value into corresponding variable.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The execution of the previously stored handler or the state
                FLOAT_INPUT in case of validation error.
        """
        try:
            value = float(update.message.text)
        except (ValueError, AssertionError):
            update.message.reply_text(
                text='Invalid value, insert a floating point number'
            )
            return BotConfig.FLOAT_INPUT

        context.bot_data[
            context.user_data[BotConfig.CURRENT_VARIABLE]
        ] = value

        return context.user_data[BotConfig.RETURN_HANDLER](update, context)

    @staticmethod
    def _end(update: Update, context: CallbackContext) -> int:
        """
        Handler to end the configuration sequence.

        Args:
            update: The update to be handled.
            context: The context object for the update.

        Returns:
            The state END.
        """
        context.user_data.clear()

        if update.callback_query:
            update.callback_query.answer()
            update.callback_query.edit_message_text(text='Configuration done.')
        else:
            update.message.reply_text(text='Configuration canceled.')

        return BotConfig.END
