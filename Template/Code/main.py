from PyQt6.QtGui import QIcon, QPixmap, QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QWidget,
    QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton,
    QMessageBox, QDialog, QFormLayout, QSpinBox, QCheckBox, QDialogButtonBox
)
from PyQt6.QtCore import Qt
import sys
# this project should use a modular approach - try to keep UI logic and game logic separate
from game_logic import Game21


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game of 21")
        self.setWindowIcon(
            QIcon(
                "./icons/game.png"))  # documentation: <a href="https://www.flaticon.com/free-icons/blackjack" title="blackjack icons">Blackjack icons created by Paul J. - Flaticon</a>

        # set the windows dimensions
        self.setGeometry(200, 200, 900, 600)

        self.game = Game21()

        # set global styles
        table_image_path = "./images/table_bg.jpg"

        # set stylesheet for the main window and its components
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #0b3b24; /* fallback */
            }}
            #centralWidget {{
                background-color: #0b3b24;
                background-image: url("{table_image_path}");
                background-repeat: no-repeat;
                background-position: center;
            }}
            QGroupBox {{
                border: 2px solid #1abc9c;
                border-radius: 10px;
                margin-top: 10px;
                color: #ecf0f1;
                font-weight: bold;
                background-color: rgba(0,0,0,0.35);
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 14px;
                padding: 0 6px;
            }}
            QLabel {{
                color: #ecf0f1;
                font-size: 13px;
            }}
            QLabel[card="true"] {{
                /* card-like rectangle */
                border: 2px solid #2c3e50;
                border-radius: 12px;

                /* keep text away from the edge */
                padding: 6px 10px;

                /* FIXED card size (prevents stretching) */
                min-width: 90px;
                max-width: 90px;
                min-height: 130px;
                max-height: 130px;            

                background-color: #ffffff;
                color: #000000;
                font-size: 22px;
                font-weight: bold;

                margin-right: 8px;
            }}
            /* red text for hearts & diamonds, without losing the card shape */
            QLabel[card="true"][red="true"] {{
                color: #e74c3c;
            }}
            QPushButton {{
                border-radius: 18px;
                padding: 10px 28px;
                font-weight: bold;
                font-size: 15px;
                color: #ffffff;
            }}
            QPushButton#hitButton {{
                background-color: #27ae60;
            }}
            QPushButton#hitButton:hover:!disabled {{
                background-color: #2ecc71;
            }}
            QPushButton#standButton {{
                background-color: #c0392b;
            }}
            QPushButton#standButton:hover:!disabled {{
                background-color: #e74c3c;
            }}
            QPushButton#newRoundButton {{
                background-color: #2980b9;
            }}
            QPushButton#newRoundButton:hover:!disabled {{
                background-color: #3498db;
            }}
            QPushButton:disabled {{
                background-color: #555555;
                color: #aaaaaa;
            }}
        """)

        self.initUI()
        # set default sizes
        self.card_font_size = 22
        self.status_font_size = 15
        self.high_contrast = False

        self.create_menu()
        self.apply_ui_sizes()

    def initUI(self):
        # Create and arrange widgets and layout. Remove pass when complete.
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # Main vertical layout
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(18, 18, 18, 18)
        mainLayout.setSpacing(10)
        central_widget.setLayout(mainLayout)

        # ------- Title banner (top) -------
        titleLabel = QLabel()
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_path = "./images/title_logo.png"
        pix = QPixmap(logo_path)

        if not pix.isNull():
            # scale smaller
            titleLabel.setPixmap(
                pix.scaledToHeight(155, Qt.TransformationMode.SmoothTransformation)
            )
            # force the QLabel height to stay tight (reduces the “box” space)
            titleLabel.setFixedHeight(145)
        else:
            titleLabel.setText("21 CARD GAME")
            title_font = titleLabel.font()
            title_font.setPointSize(22)
            title_font.setBold(True)
            titleLabel.setFont(title_font)
            titleLabel.setFixedHeight(60)

        mainLayout.addWidget(titleLabel)

        # ------- Top row: Dealer and Stats -------
        topRowLayout = QHBoxLayout()
        topRowLayout.setSpacing(10)

        topRowLayout.addStretch(1)  # left spacer

        # TODO: Dealer Section with cards
        dealerGroup = QGroupBox("Dealer")
        dealerLayout = QVBoxLayout()
        dealerLayout.setSpacing(8)
        dealerGroup.setLayout(dealerLayout)

        self.dealerCardsLayout = QHBoxLayout()
        self.dealerCardsLayout.setSpacing(6)
        dealerLayout.addLayout(self.dealerCardsLayout)

        self.dealerTotalLabel = QLabel("Dealer total: ?")
        dealerLayout.addWidget(self.dealerTotalLabel)

        topRowLayout.addWidget(dealerGroup, stretch=2)

        #  TODO: Feedback – stats panel on the right
        statsGroup = QGroupBox("Status")
        statsLayout = QVBoxLayout()
        statsLayout.setSpacing(4)
        statsGroup.setLayout(statsLayout)

        self.playerWinsLabel = QLabel("Player wins: 0")
        self.dealerWinsLabel = QLabel("Dealer wins: 0")
        self.pushesLabel = QLabel("Pushes: 0")

        statsLayout.addWidget(self.playerWinsLabel)
        statsLayout.addWidget(self.dealerWinsLabel)
        statsLayout.addWidget(self.pushesLabel)

        topRowLayout.addWidget(statsGroup, stretch=1)
        topRowLayout.addStretch(1)  # right spacer

        #  TODO: Add widgets to layout
        mainLayout.addLayout(topRowLayout)

        # ------- Middle: Status Label -------
        self.statusLabel = QLabel("Welcome to Game of 21. Click 'New Round' to start.")
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusLabel.setWordWrap(False)

        # limit the width so it doesn't stretch across the whole window
        self.statusLabel.setMaximumWidth(720)

        # set a fixed height so it doesn't grow too tall with text changes
        self.statusLabel.setFixedHeight(50)

        # limit the width so it doesn't stretch across the whole window
        self.statusLabel.setMaximumWidth(720)

        # smaller padding and font so it looks less tall
        self.statusLabel.setStyleSheet("""
            background-color: #145a32;
            color: #f1c40f;
            font-size: 14px;
            font-weight: bold;
            border-radius: 14px;
            padding: 6px 10px;
            border: 2px solid #f1c40f;
        """)

        # center the status label horizontally
        statusRow = QHBoxLayout()
        statusRow.addStretch(1)
        statusRow.addWidget(self.statusLabel)
        statusRow.addStretch(1)
        mainLayout.addLayout(statusRow)

        # TODO: Player Section with cards
        playerGroup = QGroupBox("Player")
        playerLayout = QVBoxLayout()
        playerLayout.setSpacing(5)
        playerGroup.setLayout(playerLayout)

        self.playerCardsLayout = QHBoxLayout()
        self.playerCardsLayout.setSpacing(6)
        playerLayout.addLayout(self.playerCardsLayout)

        self.playerTotalLabel = QLabel("Player total: 0")
        playerLayout.addWidget(self.playerTotalLabel)

        mainLayout.addWidget(playerGroup)

        #  TODO: Buttons for hit, stand, new round
        controlsLayout = QHBoxLayout()
        controlsLayout.setSpacing(30)
        controlsLayout.addStretch(1)

        self.hitButton = QPushButton("Hit")
        self.hitButton.setObjectName("hitButton")
        self.standButton = QPushButton("Stand")
        self.standButton.setObjectName("standButton")
        self.newRoundButton = QPushButton("New Round")
        self.newRoundButton.setObjectName("newRoundButton")

        controlsLayout.addWidget(self.hitButton)
        controlsLayout.addWidget(self.standButton)
        controlsLayout.addWidget(self.newRoundButton)

        controlsLayout.addStretch(1)
        mainLayout.addLayout(controlsLayout)

        #  TODO: Trigger a new layout with a new round
        self.hitButton.clicked.connect(self.on_hit)
        self.standButton.clicked.connect(self.on_stand)
        self.newRoundButton.clicked.connect(self.on_new_round)

        # start with no active round
        self.hitButton.setEnabled(False)
        self.standButton.setEnabled(False)

# ------- Menu creation -------
    def create_menu(self):
        menubar = self.menuBar()

        # match the game theme
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #0b3b24;
                color: #f1c40f;
                font-weight: bold;
            }
            QMenuBar::item { padding: 6px 10px; }
            QMenuBar::item:selected { background-color: #145a32; }

            QMenu {
                background-color: #0b3b24;
                color: #f1c40f;
                border: 1px solid #f1c40f;
            }
            QMenu::item { padding: 6px 18px; }
            QMenu::item:selected { background-color: #145a32; }
        """)

        game_menu = menubar.addMenu("Game")

        # New Game action
        new_game_action = QAction("New Game", self)
        new_game_action.triggered.connect(self.on_new_game)
        game_menu.addAction(new_game_action)

        game_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        game_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        about_action = QAction("About / How to Play", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)


    def on_new_game(self):
        # Restart game: reset stats + start fresh round
        self.game.player_wins = 0
        self.game.dealer_wins = 0
        self.game.pushes = 0

        self.update_score_labels()

        self.game.new_round()
        self.new_round_setup()

        self.statusLabel.setText("New game started - good luck!")
        self.set_status_style("neutral")

    # ABOUT DIALOG
    def show_about(self):
        text = (
            "Game of 21\n\n"
            "Game of 21 is a simplified Blackjack-style card game "
            "played between a player and a dealer.\n\n"

            "How to play:\n"
            "• Click 'New Round' to start.\n"
            "• You are dealt two cards.\n"
            "• Choose 'Hit' to take another card.\n"
            "• Choose 'Stand' to end your turn.\n\n"

            "Card values:\n"
            "• Number cards are worth their value (2–10).\n"
            "• Jack, Queen and King are worth 10.\n"
            "• Ace is worth 1 or 11, whichever is better for the hand.\n\n"

            "Dealer rules:\n"
            "• The dealer must hit until their total is at least 17.\n\n"

            "Winning:\n"
            "• The closest hand to 21 without going over wins.\n"
            "• If both totals are the same, the round is a push (tie).\n\n"

            "Main features:\n"
            "• Visual card display for player and dealer.\n"
            "• Clear win / lose / push feedback.\n"
            "• Simple statistics showing wins, losses and ties."
        )

        QMessageBox.information(self, "About Game of 21", text)
    # UI SIZE ADJUSTMENTS
    def apply_ui_sizes(self):
        border_color = "#000000" if self.high_contrast else "#2c3e50"
        border_width = "3px" if self.high_contrast else "2px"

        # append a small rule override so we can adjust sizes without rewriting all CSS
        self.setStyleSheet(self.styleSheet() + f"""
                QLabel[card="true"] {{
                    border: {border_width} solid {border_color};
                    font-size: {self.card_font_size}px;
                }}
            """)

        if hasattr(self, "statusLabel"):
            self.statusLabel.setWordWrap(False)
            self.statusLabel.setStyleSheet(self.statusLabel.styleSheet() + f"""
                    font-size: {self.status_font_size}px;
                    padding: 2px 10px;
                """)

    # BUTTON ACTIONS
    def on_hit(self):
        # Player takes a card
        card = self.game.player_hit()
        self.add_card(self.playerCardsLayout, card)

        self.update_player_total_label()

        if self.game.player_total() > 21:
            # TODO: what should happen if a player goes over 21? Remove pass when complete
            # player busts: reveal dealer, decide winner and end round
            self.update_dealer_cards(full=True)
            result_text = self.game.decide_winner()
            self.statusLabel.setText(result_text)
            self.set_status_style(result_text)
            self.update_score_labels()
            self.end_round()

    def on_stand(self):
        # TODO: Player ends turn; dealer reveals their hidden card and plays. Remove pass when complete
        # reveal dealer hidden card
        self.update_dealer_cards(full=True)

        # dealer plays according to rules
        self.game.play_dealer_turn()
        self.update_dealer_cards(full=True)

        # decide winner and show status
        result_text = self.game.decide_winner()
        self.statusLabel.setText(result_text)
        self.set_status_style(result_text)
        self.update_score_labels()

        # end round
        self.end_round()

    def on_new_round(self):
        self.game.new_round()
        self.new_round_setup()

    # HELPER METHODS
    def clear_layout(self, layout):
        # Remove all widgets from a layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, layout, card_text):
        # Create a QLabel showing the card value and add it to the chosen layout.
        label = QLabel(card_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setProperty("card", True)

        # mark hearts/diamonds as red using a property (keeps card shape style)
        if card_text not in ("??", ""):
            suit = card_text[-1]
            if suit in ("♥", "♦"):
                label.setProperty("red", True)

        layout.addWidget(label)

    def update_dealer_cards(self, full=False):
        # Show dealer cards; hide the first card until revealed
        self.clear_layout(self.dealerCardsLayout)

        for i, card in enumerate(self.game.dealer_hand):
            if i == 0 and not full:
                self.add_card(self.dealerCardsLayout, "??")  # face-down
            else:
                self.add_card(self.dealerCardsLayout, card)

        # TODO: update relevant labels in response to dealer actions. Remove pass when complete
        if full:
            self.dealerTotalLabel.setText(
                f"Dealer total: {self.game.dealer_total()}"
            )
        else:
            self.dealerTotalLabel.setText("Dealer total: ?")

    def update_player_total_label(self):
        total = self.game.player_total()
        self.playerTotalLabel.setText(
            f"Player total: <span style='color:#f1c40f; font-weight:bold'>{total}</span>"
        )
        self.playerTotalLabel.setTextFormat(Qt.TextFormat.RichText)

    def new_round_setup(self):
        # TODO: Prepare a fresh visual layout
        self.clear_layout(self.playerCardsLayout)
        self.clear_layout(self.dealerCardsLayout)

        # deal initial cards into the model
        self.game.deal_initial_cards()

        # TODO: update relevant labels (reset dealer and player totals)
        for card in self.game.player_hand:
            self.add_card(self.playerCardsLayout, card)

        self.update_dealer_cards(full=False)
        self.update_player_total_label()
        self.dealerTotalLabel.setText("Dealer total: ?")

        self.statusLabel.setText("Your turn - choose Hit or Stand")
        self.set_status_style("neutral")

        # TODO: display new cards for dealers and players
        # already handled above

        # TODO: enable buttons for Stand and Hit - Remove pass when complete
        self.hitButton.setEnabled(True)
        self.standButton.setEnabled(True)
        self.newRoundButton.setEnabled(False)

    def end_round(self):
        # TODO: Disable button actions after the round ends. Remove pass when complete
        self.hitButton.setEnabled(False)
        self.standButton.setEnabled(False)
        self.newRoundButton.setEnabled(True)

    def update_score_labels(self):
        # helper to sync labels with game logic stats
        self.playerWinsLabel.setText(f"Player wins: {self.game.player_wins}")
        self.dealerWinsLabel.setText(f"Dealer wins: {self.game.dealer_wins}")
        self.pushesLabel.setText(f"Pushes: {self.game.pushes}")

    def set_status_style(self, result_text: str):
        # small helper to visually emphasise result
        if isinstance(result_text, str) and (
                "Player busts" in result_text or result_text.startswith("Dealer wins")
        ):
            bg = "#7f1d1d"  # red-ish for bad outcome
            border = "#e74c3c"
        elif isinstance(result_text, str) and (
                "Dealer busts" in result_text or result_text.startswith("Player wins")
        ):
            bg = "#145a32"  # green-ish for good outcome
            border = "#2ecc71"
        elif isinstance(result_text, str) and "Push" in result_text:
            bg = "#7f6a1d"  # neutral
            border = "#f1c40f"
        else:
            bg = "#145a32"
            border = "#f1c40f"

        self.statusLabel.setStyleSheet(f"""
            background-color: {bg};
            color: #f9f9f9;
            font-size: 18px;
            font-weight: bold;
            border-radius: 16px;
            padding: 10px 18px;
            border: 2px solid {border};
        """)


# complete

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # macOS only fix for icons appearing
    app.setAttribute(Qt.ApplicationAttribute.AA_DontShowIconsInMenus, False)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
